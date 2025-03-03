import os
import sqlite3
import faiss
import numpy as np

class CodeDB:
    def __init__(self, db_path="code_grasp.db", index_path="code_grasp.faiss"):
        self.db_path = db_path
        self.index_path = index_path
        
        # The dimension will be set when we connect and create/load the index
        self.dim = None  
        self.connect()

    def connect(self):
        """Initialize SQLite and FAISS."""
        self.conn = sqlite3.connect(self.db_path)
        self.cursor = self.conn.cursor()
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS code (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                file_path TEXT UNIQUE,
                file_language TEXT,
                embedding_id INTEGER,
                added_on TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Add a metadata table if it doesn't exist
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS metadata (
                key TEXT PRIMARY KEY,
                value TEXT
            )
        """)
        self.conn.commit()
        
        if os.path.exists(self.index_path):
            self.index = faiss.read_index(self.index_path)
            self.dim = self.index.d
            
            # Get stored dimension from metadata
            self.cursor.execute("SELECT value FROM metadata WHERE key = 'embedding_dim'")
            result = self.cursor.fetchone()
            if result:
                self.dim = int(result[0])
        else:
            # Default to the Qodo-Embed dimension, but this will be updated 
            # when adding embeddings if using the fallback model
            self.dim = 1536
            
            # Using IndexFlatIP for cosine similarity since embeddings are normalized
            self.index = faiss.IndexFlatIP(self.dim)
            
            # Store dimension in metadata
            self.cursor.execute("INSERT OR REPLACE INTO metadata (key, value) VALUES (?, ?)", 
                               ('embedding_dim', str(self.dim)))
            self.conn.commit()

    def add_embeddings(self, embeddings, file_paths):
        """Store embeddings and metadata."""
        if len(embeddings) == 0:
            return
            
        # Check if the dimension matches our current index
        embedding_dim = embeddings.shape[1]
        if self.dim is None:
            # First time adding embeddings, set the dimension
            self.dim = embedding_dim
            self.index = faiss.IndexFlatIP(self.dim)
            
            # Store dimension in metadata
            self.cursor.execute("INSERT OR REPLACE INTO metadata (key, value) VALUES (?, ?)", 
                               ('embedding_dim', str(self.dim)))
            self.conn.commit()
        elif self.dim != embedding_dim:
            # Dimension mismatch - this could happen if switching between models
            # We need to recreate the index
            print(f"Warning: Embedding dimension mismatch. Expected {self.dim}, got {embedding_dim}.")
            print("Recreating the index with the new dimension.")
            
            # Create a new index with the new dimension
            self.index = faiss.IndexFlatIP(embedding_dim)
            self.dim = embedding_dim
            
            # Update the metadata
            self.cursor.execute("INSERT OR REPLACE INTO metadata (key, value) VALUES (?, ?)", 
                               ('embedding_dim', str(self.dim)))
                               
            # Clear the existing database entries since they won't match the new index
            self.cursor.execute("DELETE FROM code")
            self.conn.commit()
            
        # Get file extensions to determine language
        file_languages = []
        for path in file_paths:
            ext = os.path.splitext(path)[1].lower()
            
            # Map extensions to languages
            language_map = {
                ".py": "Python",
                ".cpp": "C++", ".hpp": "C++", ".h": "C++", ".c": "C++",
                ".cs": "C#",
                ".go": "Go",
                ".java": "Java",
                ".js": "Javascript",
                ".php": "PHP",
                ".rb": "Ruby",
                ".ts": "Typescript"
            }
            
            file_languages.append(language_map.get(ext, "Unknown"))
        
        # Get current number of embeddings in the index
        start_id = self.index.ntotal
        
        # Add to FAISS index
        self.index.add(embeddings)
        
        # Add to SQLite
        for i, (path, language) in enumerate(zip(file_paths, file_languages)):
            embedding_id = start_id + i
            self.cursor.execute(
                "INSERT OR REPLACE INTO code (file_path, file_language, embedding_id) VALUES (?, ?, ?)", 
                (path, language, embedding_id)
            )
        
        self.conn.commit()
        faiss.write_index(self.index, self.index_path)

    def search(self, query_embedding, k=5):
        """Find k nearest embeddings using cosine similarity."""
        if self.index.ntotal == 0:
            return []
        
        # Check if the query embedding has the right dimension
        if query_embedding.shape[1] != self.dim:
            print(f"Error: Query embedding dimension {query_embedding.shape[1]} doesn't match index dimension {self.dim}")
            return []
            
        # Normalize the query embedding for cosine similarity
        query_embedding_norm = query_embedding / np.linalg.norm(query_embedding)
        
        # Using dot product because we're using IndexFlatIP
        # Higher scores are better in this case (more similar)
        scores, indices = self.index.search(query_embedding_norm, k)
        
        results = []
        for idx, score in zip(indices[0], scores[0]):
            if idx != -1:  # Valid index
                self.cursor.execute("SELECT file_path, file_language FROM code WHERE embedding_id = ?", (int(idx),))
                result = self.cursor.fetchone()
                if result:
                    file_path, file_language = result
                    # Convert the score to a similarity value between 0 and 1
                    similarity = float(score)
                    results.append((file_path, file_language, similarity))
        
        return results

    def close(self):
        """Close the database connection."""
        self.conn.close()