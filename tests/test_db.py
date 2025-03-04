"""
Tests for the database module
"""
import os
import unittest
import tempfile
import sys
import gc
import numpy as np
import pytest

from code_grasp.db import CodeDB

# Skip tests on macOS CI environment to avoid segmentation faults
skip_on_macos_ci = pytest.mark.skipif(
    sys.platform == "darwin" and os.environ.get("CI") == "true",
    reason="Skip on macOS CI to avoid segmentation faults with PyTorch/FAISS",
)


class TestCodeDB(unittest.TestCase):
    """Tests for the CodeDB class"""
    
    def setUp(self):
        """Set up test fixtures"""
        # Create temporary database and index files
        self.temp_dir = tempfile.TemporaryDirectory()
        self.db_path = os.path.join(self.temp_dir.name, "test.db")
        self.index_path = os.path.join(self.temp_dir.name, "test.faiss")
        self.db = CodeDB(db_path=self.db_path, index_path=self.index_path)
    
    def tearDown(self):
        """Tear down test fixtures"""
        self.db.close()
        self.temp_dir.cleanup()
        
        # Force garbage collection to prevent memory issues
        gc.collect()
        
        # Sleep briefly to allow resources to be properly released
        import time
        time.sleep(0.1)
    
    @skip_on_macos_ci
    def test_initialization(self):
        """Test that database initializes correctly"""
        # Check that the database was created
        self.assertTrue(os.path.exists(self.db_path))
        # Index file is created only after adding embeddings
    
    @skip_on_macos_ci
    def test_add_and_search(self):
        """Test adding embeddings and searching"""
        # Create some sample embeddings and file paths
        embeddings = np.random.rand(3, 384).astype(np.float32)
        
        # Normalize embeddings
        for i in range(embeddings.shape[0]):
            embeddings[i] = embeddings[i] / np.linalg.norm(embeddings[i])
            
        file_paths = [
            "/path/to/file1.py",
            "/path/to/file2.js",
            "/path/to/file3.rb"
        ]
        
        # Add embeddings to database
        self.db.add_embeddings(embeddings, file_paths)
        
        # Check that index file was created
        self.assertTrue(os.path.exists(self.index_path))
        
        # Search for similar embeddings
        query_embedding = embeddings[0:1]  # Use first embedding as query
        results = self.db.search(query_embedding, k=2)
        
        # Should find at least one result (itself)
        self.assertTrue(len(results) > 0)
        
        # First result should have high similarity (it's the same embedding)
        self.assertGreater(results[0][2], 0.99)


if __name__ == '__main__':
    unittest.main()
