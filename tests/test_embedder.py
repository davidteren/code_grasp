"""
Tests for the embedder module
"""
import os
import unittest
import numpy as np
from code_grasp.embedder import Embedder


class TestEmbedder(unittest.TestCase):
    """Tests for the Embedder class"""
    
    def setUp(self):
        """Set up test fixtures"""
        # Always use lightweight mode for tests to avoid large model downloads
        self.embedder = Embedder(force_lightweight=True)
    
    def test_initialization(self):
        """Test that embedder initializes correctly"""
        self.assertTrue(self.embedder.is_fallback)
        self.assertEqual(self.embedder.embedding_dim, 384)  # Lightweight model dimension
    
    def test_embed_text(self):
        """Test embedding a simple text sample"""
        text = "def fibonacci(n):\n    if n <= 1:\n        return n\n    else:\n        return fibonacci(n-1) + fibonacci(n-2)"
        embedding = self.embedder.embed(text)
        
        # Check shape and normalization
        self.assertEqual(embedding.shape, (1, 384))
        self.assertAlmostEqual(np.linalg.norm(embedding), 1.0, places=5)
    
    def test_embed_batch(self):
        """Test embedding a batch of text samples"""
        texts = [
            "def add(a, b):\n    return a + b",
            "class Node:\n    def __init__(self, value):\n        self.value = value\n        self.next = None"
        ]
        embeddings = self.embedder.embed_batch(texts, batch_size=2)
        
        # Check shape and normalization
        self.assertEqual(embeddings.shape, (2, 384))
        for i in range(embeddings.shape[0]):
            self.assertAlmostEqual(np.linalg.norm(embeddings[i]), 1.0, places=5)


if __name__ == '__main__':
    unittest.main()
