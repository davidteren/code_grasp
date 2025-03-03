import os
import click
import faiss
import numpy as np
import gc
from .embedder import Embedder
from .db import CodeDB

def get_embedder(lightweight):
    """Get an embedder instance with appropriate settings."""
    return Embedder(force_lightweight=lightweight)

@click.group()
def cli():
    """Code Grasp: Analyze code with embedding models."""
    pass

@cli.command()
@click.argument("question")
@click.option("--lightweight", is_flag=True, help="Force using the lightweight model")
def ask(question, lightweight):
    """Ask a question about current knowledge."""
    click.echo(f"Processing your question: '{question}'")
    
    try:
        embedder = get_embedder(lightweight)
        db = CodeDB()
        
        # Embed the question
        query_embedding = embedder.embed(question)
        results = db.search(query_embedding, k=5)
        
        if not results:
            click.echo("No relevant code in the database yet. Add a directory first!")
        else:
            click.echo("\nTop matches:")
            for file_path, language, similarity in results:
                # Format similarity as percentage
                similarity_pct = similarity * 100
                click.echo(f"- [{language}] {file_path} (similarity: {similarity_pct:.2f}%)")
                
                # Show a snippet of the code if available
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                    
                    # Get first 5 non-empty lines as preview
                    lines = [line for line in content.split('\n') if line.strip()]
                    preview = '\n'.join(lines[:5])
                    
                    if preview:
                        click.echo("\nPreview:")
                        click.echo("```")
                        click.echo(preview)
                        if len(lines) > 5:
                            click.echo("...")
                        click.echo("```\n")
                except Exception as e:
                    click.echo(f"  Could not display preview: {e}")
        
        db.close()
    except Exception as e:
        click.echo(f"Error: {e}")

@cli.command()
@click.argument("directory", type=click.Path(exists=True))
@click.option("--lightweight", is_flag=True, help="Force using the lightweight model")
@click.option("--batch-size", type=int, default=4, help="Batch size for processing files")
def add(directory, lightweight, batch_size):
    """Add a directory of code files to analyze."""
    click.echo(f"Processing directory: {directory}")
    
    try:
        embedder = get_embedder(lightweight)
        
        if embedder.is_fallback:
            click.echo("Using lightweight model for embedding.")
            
        db = CodeDB()
        
        click.echo("Embedding files (this may take a while for large directories)...")
        embeddings, file_paths = embedder.embed_files_in_dir(directory, batch_size=batch_size)
        
        if len(file_paths) == 0:
            click.echo("No supported code files were successfully processed in the directory.")
        else:
            db.add_embeddings(embeddings, file_paths)
            click.echo(f"Added {len(file_paths)} files from {directory}")
            
            # Show breakdown by language
            language_counts = {}
            for path in file_paths:
                ext = os.path.splitext(path)[1].lower()
                language_map = {
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
                language = language_map.get(ext, "Unknown")
                language_counts[language] = language_counts.get(language, 0) + 1
            
            click.echo("\nFiles by language:")
            for language, count in language_counts.items():
                click.echo(f"- {language}: {count} files")
        
        db.close()
        
        # Force garbage collection
        gc.collect()
    except Exception as e:
        click.echo(f"Error: {e}")

@cli.command(name="ask-dir")
@click.argument("directory", type=click.Path(exists=True))
@click.argument("question")
@click.option("--lightweight", is_flag=True, help="Force using the lightweight model")
@click.option("--batch-size", type=int, default=4, help="Batch size for processing files")
def ask_dir(directory, question, lightweight, batch_size):
    """Ask a question about code in a specific directory."""
    click.echo(f"Analyzing directory: {directory}")
    click.echo(f"Question: {question}")
    
    try:
        embedder = get_embedder(lightweight)
        
        if embedder.is_fallback:
            click.echo("Using lightweight model for embedding.")
            
        # Embed the files in the directory
        click.echo("Embedding files (this may take a while for large directories)...")
        embeddings, file_paths = embedder.embed_files_in_dir(directory, batch_size=batch_size)
        
        if len(file_paths) == 0:
            click.echo("No supported code files were successfully processed in the directory.")
            return
            
        # Embed the question
        query_embedding = embedder.embed(question)
        
        # Check if we have any embeddings
        if embeddings.shape[0] == 0:
            click.echo("No files could be embedded from the directory.")
            return
            
        # Create a temporary FAISS index for this query
        dim = embeddings.shape[1]
        index = faiss.IndexFlatIP(dim)  # Using IP for cosine similarity
        
        # Use the appropriate dimension
        if query_embedding.shape[1] != dim:
            click.echo(f"Warning: Query embedding dimension ({query_embedding.shape[1]}) doesn't match file embeddings dimension ({dim}).")
            # Create a zero embedding of the correct dimension
            query_embedding = np.zeros((1, dim))
        
        # Add embeddings to index
        index.add(embeddings)
        
        # Search for similar files
        k = min(5, len(file_paths))  # Return at most 5 results
        scores, indices = index.search(query_embedding, k)
        
        click.echo(f"\nTop matches in {directory}:")
        for idx, score in zip(indices[0], scores[0]):
            if idx != -1 and idx < len(file_paths):
                path = file_paths[idx]
                ext = os.path.splitext(path)[1].lower()
                language_map = {
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
                language = language_map.get(ext, "Unknown")
                similarity_pct = score * 100
                
                click.echo(f"- [{language}] {path} (similarity: {similarity_pct:.2f}%)")
                
                # Show a snippet of the code if available
                try:
                    with open(path, 'r', encoding='utf-8') as f:
                        content = f.read()
                    
                    # Get first 5 non-empty lines as preview
                    lines = [line for line in content.split('\n') if line.strip()]
                    preview = '\n'.join(lines[:5])
                    
                    if preview:
                        click.echo("\nPreview:")
                        click.echo("```")
                        click.echo(preview)
                        if len(lines) > 5:
                            click.echo("...")
                        click.echo("```\n")
                except Exception as e:
                    click.echo(f"  Could not display preview: {e}")
                    
        # Force garbage collection
        gc.collect()
    except Exception as e:
        click.echo(f"Error: {e}")

@cli.command()
def info():
    """Display information about the stored embeddings."""
    try:
        # First, check if the embedder can load
        embedder = get_embedder(False)  # Try the full model first
        if embedder.is_fallback:
            model_name = "Sentence-Transformers (lightweight)"
        else:
            model_name = "Qodo-Embed-1-1.5B"
            
        embedding_dim = embedder.embedding_dim
        
        click.echo(f"Current model: {model_name}")
        click.echo(f"Embedding dimension: {embedding_dim}")
        
        # Device information
        click.echo(f"Device: {embedder.device}")
        
        # Print memory usage for MPS/CUDA devices
        if torch.backends.mps.is_available():
            click.echo("Memory metrics not available for MPS device")
        elif torch.cuda.is_available():
            click.echo(f"CUDA memory allocated: {torch.cuda.memory_allocated() / 1024**2:.2f} MB")
            click.echo(f"CUDA memory reserved: {torch.cuda.memory_reserved() / 1024**2:.2f} MB")
        
        db = CodeDB()
        
        # Get total count of files
        db.cursor.execute("SELECT COUNT(*) FROM code")
        count = db.cursor.fetchone()[0]
        
        if count == 0:
            click.echo("No files have been added yet. Use 'code_grasp add <directory>' to add files.")
            db.close()
            return
            
        click.echo(f"Total files in database: {count}")
        
        # Get language breakdown
        db.cursor.execute("SELECT file_language, COUNT(*) FROM code GROUP BY file_language ORDER BY COUNT(*) DESC")
        language_counts = db.cursor.fetchall()
        
        click.echo("\nFiles by language:")
        for language, language_count in language_counts:
            click.echo(f"- {language}: {language_count} files")
            
        # Get index size
        index_size_mb = os.path.getsize(db.index_path) / (1024 * 1024) if os.path.exists(db.index_path) else 0
        db_size_mb = os.path.getsize(db.db_path) / (1024 * 1024) if os.path.exists(db.db_path) else 0
        
        click.echo(f"\nDatabase size: {db_size_mb:.2f} MB")
        click.echo(f"Index size: {index_size_mb:.2f} MB")
        
        db.close()
    except Exception as e:
        click.echo(f"Error: {e}")

if __name__ == "__main__":
    cli()