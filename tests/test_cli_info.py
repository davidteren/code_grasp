"""
Tests for the CLI info command
"""
import unittest
import os
import sys
import gc
from unittest.mock import patch, MagicMock
from click.testing import CliRunner
import torch
import pytest

from code_grasp.cli import info

# Skip tests on macOS CI environment to avoid segmentation faults
skip_on_macos_ci = pytest.mark.skipif(
    sys.platform == "darwin" and os.environ.get("CI") == "true",
    reason="Skip on macOS CI to avoid segmentation faults with PyTorch/FAISS",
)


class TestCLIInfo(unittest.TestCase):
    """Tests for the CLI info command."""

    def tearDown(self):
        """Clean up resources after tests"""
        # Force garbage collection
        gc.collect()
        torch.cuda.empty_cache() if torch.cuda.is_available() else None
    
    @skip_on_macos_ci
    @patch('code_grasp.cli.get_embedder')
    @patch('code_grasp.cli.CodeDB')
    @patch('torch.backends.mps.is_available')
    def test_info_uses_lightweight_on_mps(self, mock_mps_available, mock_db, mock_get_embedder):
        """Test that info uses lightweight model on MPS devices."""
        # Setup mocks
        mock_mps_available.return_value = True
        mock_embedder = MagicMock()
        mock_embedder.is_fallback = True
        mock_embedder.embedding_dim = 384
        mock_embedder.device = torch.device("mps")
        mock_get_embedder.return_value = mock_embedder
        
        # Mock DB cursor and methods
        mock_db_instance = mock_db.return_value
        mock_db_instance.cursor = MagicMock()
        mock_db_instance.cursor.execute = MagicMock()
        mock_db_instance.cursor.fetchone = MagicMock(return_value=[0])  # No files
        mock_db_instance.index_path = "test.faiss"
        mock_db_instance.db_path = "test.db"
        
        # Run command
        runner = CliRunner()
        result = runner.invoke(info)
        
        # Verify
        self.assertEqual(result.exit_code, 0)
        # Check that get_embedder was called with lightweight=True
        mock_get_embedder.assert_called_once_with(True)
        # Check output contains expected text
        self.assertIn("Using lightweight model on Apple Silicon", result.output)
        self.assertIn("Current model: Sentence-Transformers (lightweight)", result.output)

    @skip_on_macos_ci
    @patch('code_grasp.cli.get_embedder')
    @patch('code_grasp.cli.CodeDB')
    @patch('torch.backends.mps.is_available')
    @patch('torch.cuda.is_available')
    def test_info_respects_lightweight_flag(self, mock_cuda_available, mock_mps_available, mock_db, mock_get_embedder):
        """Test that info respects --lightweight flag on non-MPS devices."""
        # Setup mocks
        mock_mps_available.return_value = False
        mock_cuda_available.return_value = False
        
        mock_embedder = MagicMock()
        mock_embedder.is_fallback = True
        mock_embedder.embedding_dim = 384
        mock_embedder.device = torch.device("cpu")
        mock_get_embedder.return_value = mock_embedder
        
        # Mock DB cursor and methods
        mock_db_instance = mock_db.return_value
        mock_db_instance.cursor = MagicMock()
        mock_db_instance.cursor.execute = MagicMock()
        mock_db_instance.cursor.fetchone = MagicMock(return_value=[0])  # No files
        mock_db_instance.index_path = "test.faiss"
        mock_db_instance.db_path = "test.db"
        
        # Run command with --lightweight flag
        runner = CliRunner()
        result = runner.invoke(info, ['--lightweight'])
        
        # Verify
        self.assertEqual(result.exit_code, 0)
        # Check that get_embedder was called with lightweight=True
        mock_get_embedder.assert_called_once_with(True)
        # Check output contains expected text
        self.assertIn("Current model: Sentence-Transformers (lightweight)", result.output)

if __name__ == '__main__':
    unittest.main()
