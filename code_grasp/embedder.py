import os
import torch
import torch.nn.functional as F
import numpy as np
import gc
from transformers import AutoTokenizer, AutoModel

class Embedder:
    def __init__(self, force_lightweight=False):
        """
        Initialize the embedder with appropriate model.
        
        Args:
            force_lightweight: If True, will skip trying to load Qodo-Embed and use the lightweight model directly
        """
        self.is_fallback = force_lightweight
        
        if not force_lightweight:
            try:
                print("Attempting to load Qodo-Embed-1-1.5B model...")
                # Try to load the Qodo model with minimal memory footprint
                self.tokenizer = AutoTokenizer.from_pretrained(
                    "Qodo/Qodo-Embed-1-1.5B", 
                    trust_remote_code=True,
                    low_cpu_mem_usage=True
                )
                
                # Use very aggressive memory optimization settings
                self.model = AutoModel.from_pretrained(
                    "Qodo/Qodo-Embed-1-1.5B", 
                    trust_remote_code=True,
                    low_cpu_mem_usage=True,
                    torch_dtype=torch.float16  # Use half precision
                )
                self.is_fallback = False
                print("Successfully loaded Qodo-Embed-1-1.5B model.")
            except Exception as e:
                print(f"Warning: Could not load Qodo-Embed model: {e}")
                print("Falling back to a lightweight embedding model.")
                self.is_fallback = True
                # Free up memory
                gc.collect()
                torch.cuda.empty_cache() if torch.cuda.is_available() else None
                
        if self.is_fallback:
            # Use a much smaller model as fallback
            self.tokenizer = AutoTokenizer.from_pretrained("sentence-transformers/all-MiniLM-L6-v2")
            self.model = AutoModel.from_pretrained("sentence-transformers/all-MiniLM-L6-v2")
        
        # Use MPS (Metal Performance Shaders) on M1 Macs if available
        if torch.backends.mps.is_available():
            self.device = torch.device("mps")
            print("Using MPS (M1/M2 GPU) acceleration")
        elif torch.cuda.is_available():
            self.device = torch.device("cuda")
            print("Using CUDA acceleration")
        else:
            self.device = torch.device("cpu")
            print("Using CPU for computation")
            
        self.model.to(self.device)
        self.model.eval()
        
        # Set embedding dimension based on model
        if self.is_fallback:
            self.embedding_dim = 384  # For all-MiniLM-L6-v2
            self.max_length = 512
        else:
            self.embedding_dim = 1536  # For Qodo-Embed-1-1.5B
            self.max_length = 4096  # Reduced from 8192 to save memory
        
    def mean_pooling(self, model_output, attention_mask):
        """
        Mean pooling for fallback model (all-MiniLM-L6-v2)
        """
        token_embeddings = model_output.last_hidden_state
        input_mask_expanded = attention_mask.unsqueeze(-1).expand(token_embeddings.size()).float()
        return torch.sum(token_embeddings * input_mask_expanded, 1) / torch.clamp(input_mask_expanded.sum(1), min=1e-9)

    def last_token_pool(self, last_hidden_states, attention_mask):
        """
        Pool the last token's embedding as per Qodo-Embed docs.
        """
        left_padding = (attention_mask[:, -1].sum() == attention_mask.shape[0])
        if left_padding:
            return last_hidden_states[:, -1]
        else:
            sequence_lengths = attention_mask.sum(dim=1) - 1
            batch_size = last_hidden_states.shape[0]
            return last_hidden_states[torch.arange(batch_size, device=last_hidden_states.device), sequence_lengths]

    def embed(self, text):
        """Generate an embedding for a single text input."""
        try:
            # Truncate very long texts to avoid memory issues
            if isinstance(text, str) and len(text) > self.max_length * 4:
                text = text[:self.max_length * 4]
                
            inputs = self.tokenizer(text, max_length=self.max_length, padding=True, truncation=True, return_tensors="pt").to(self.device)
            
            with torch.no_grad():
                outputs = self.model(**inputs)
                
                # Use appropriate pooling method based on model
                if self.is_fallback:
                    embedding = self.mean_pooling(outputs, inputs['attention_mask'])
                else:
                    embedding = self.last_token_pool(outputs.last_hidden_state, inputs['attention_mask'])
                    
                # Normalize the embedding
                embedding = F.normalize(embedding, p=2, dim=1)
                
                # Free up memory immediately
                del outputs
                del inputs
                torch.cuda.empty_cache() if torch.cuda.is_available() else None
                
            return embedding.cpu().numpy()
        except Exception as e:
            print(f"Error in embed: {e}")
            # Return a zero embedding as fallback
            if self.is_fallback:
                return np.zeros((1, 384))
            else:
                return np.zeros((1, 1536))

    def embed_batch(self, texts, batch_size=4):
        """Generate embeddings for a batch of text inputs with memory-efficient batching."""
        all_embeddings = []
        
        # Process in small batches to avoid memory issues
        for i in range(0, len(texts), batch_size):
            batch_texts = texts[i:i+batch_size]
            
            # Truncate very long texts
            batch_texts = [text[:self.max_length * 4] if isinstance(text, str) and len(text) > self.max_length * 4 else text 
                           for text in batch_texts]
            
            try:
                inputs = self.tokenizer(batch_texts, max_length=self.max_length, padding=True, truncation=True, return_tensors="pt").to(self.device)
                
                with torch.no_grad():
                    outputs = self.model(**inputs)
                    
                    # Use appropriate pooling method based on model
                    if self.is_fallback:
                        embeddings = self.mean_pooling(outputs, inputs['attention_mask'])
                    else:
                        embeddings = self.last_token_pool(outputs.last_hidden_state, inputs['attention_mask'])
                        
                    # Normalize the embeddings
                    embeddings = F.normalize(embeddings, p=2, dim=1)
                    
                    # Move to CPU and convert to numpy
                    embeddings = embeddings.cpu().numpy()
                    all_embeddings.append(embeddings)
                    
                    # Free memory
                    del outputs
                    del inputs
                    torch.cuda.empty_cache() if torch.cuda.is_available() else None
                    gc.collect()
                    
            except Exception as e:
                print(f"Error in batch {i}:{i+batch_size}: {e}")
                # Return zero embeddings for this batch
                zeros = np.zeros((len(batch_texts), self.embedding_dim))
                all_embeddings.append(zeros)
        
        # Concatenate all batches
        if all_embeddings:
            return np.vstack(all_embeddings)
        else:
            return np.array([]).reshape(0, self.embedding_dim)

    def embed_files_in_dir(self, directory, batch_size=4):
        """Embed all code files in a directory using memory-efficient batching."""
        file_contents = []
        file_paths = []
        
        # These are the file extensions for the languages supported by Qodo-Embed
        supported_extensions = {
            ".py": "Python",
            ".cpp": "C++", ".hpp": "C++", ".h": "C++", ".c": "C++",
            ".cs": "C#",
            ".go": "Go",
            ".java": "Java",
            ".js": "Javascript",
            ".php": "PHP",
            ".rb": "Ruby",
            ".ts": "Typescript",
            ".jsx": "Javascript", ".tsx": "Typescript",  # Add React file types
            ".html": "HTML", ".css": "CSS"  # Add web file types
        }
        
        total_files = 0
        processed_files = 0
        skipped_files = 0
        
        # First, collect all supported files
        for root, _, files in os.walk(directory):
            for file in files:
                ext = os.path.splitext(file)[1].lower()
                if ext in supported_extensions:
                    total_files += 1
        
        if total_files == 0:
            print("No supported files found in directory.")
            return np.array([]).reshape(0, self.embedding_dim), file_paths
            
        print(f"Found {total_files} supported files in directory.")
        
        # Now process the files in batches
        for root, _, files in os.walk(directory):
            for file in files:
                ext = os.path.splitext(file)[1].lower()
                if ext in supported_extensions:
                    path = os.path.join(root, file)
                    try:
                        with open(path, "r", encoding="utf-8") as f:
                            code = f.read()
                        
                        # Skip empty files
                        if not code.strip():
                            skipped_files += 1
                            continue
                            
                        file_contents.append(code)
                        file_paths.append(path)
                        
                        processed_files += 1
                        if processed_files % 10 == 0:
                            print(f"Processed {processed_files}/{total_files} files...")
                        
                        # Process in batches to avoid memory issues
                        if len(file_contents) >= batch_size:
                            embeddings_batch = self.embed_batch(file_contents, batch_size)
                            
                            # Clear the batch after processing
                            file_contents = []
                            gc.collect()
                            
                    except Exception as e:
                        print(f"Error processing {path}: {e}")
                        skipped_files += 1
        
        # Process any remaining files
        embeddings = None
        if file_contents:
            embeddings = self.embed_batch(file_contents, batch_size)
            
        print(f"Successfully processed {processed_files - skipped_files}/{total_files} files. Skipped {skipped_files} files.")
        
        # If no files were processed, return empty arrays
        if embeddings is None or embeddings.shape[0] == 0:
            return np.array([]).reshape(0, self.embedding_dim), file_paths
            
        return embeddings, file_paths