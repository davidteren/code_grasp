# Code Grasp

A CLI tool that uses the [Qodo-Embed-1-1.5B](https://huggingface.co/Qodo/Qodo-Embed-1-1.5B) embedding model to analyze code, query knowledge, and understand code repositories.
> **⚠️ ALPHA RELEASE**: This tool is currently in alpha status and not production-ready. Use at your own risk.

## Features
1. **Code Embedding**: Generate embeddings for code files using pre-trained models
2. **Query Current Knowledge**: Ask questions about embedded code or general info the model knows
3. **Directory Analysis**: Provide a directory, embed all code files, and ask questions about them
4. **Memory-Efficient Processing**: Options to control memory usage for different hardware profiles

## Development Status

This development branch contains work-in-progress features that are not yet ready for release. Current development focuses on:

- Improving memory management
- Adding support for more programming languages
- Enhancing query capabilities
- Optimizing performance on different hardware platforms

## Installation

```bash
# Create virtual env
python3 -m venv venv
source venv/bin/activate

# Install core dependencies first
pip install torch
pip install click transformers faiss-cpu numpy accelerate

# Install package locally
pip install -e .
```

## Usage

1. **Add a Directory**:
   ```bash
   # Standard mode (will try to use Qodo-Embed-1-1.5B if possible)
   code_grasp add /path/to/code/dir
   
   # Lightweight mode (good for memory-constrained systems)
   code_grasp add --lightweight /path/to/code/dir
   
   # Control batch size for better memory management
   code_grasp add --batch-size 2 /path/to/code/dir
   ```

2. **Ask About Current Knowledge**:
   ```bash
   # Standard mode
   code_grasp ask "How do I implement a binary search?"
   
   # Lightweight mode
   code_grasp ask --lightweight "How do I implement a binary search?"
   ```

3. **Ask About a Directory**:
   ```bash
   # Standard mode
   code_grasp ask-dir /path/to/code/dir "What functions handle authentication?"
   
   # Lightweight mode with smaller batch size
   code_grasp ask-dir --lightweight --batch-size 2 /path/to/code/dir "What functions handle authentication?"
   ```

4. **Display Information**:
   ```bash
   code_grasp info
   
   # Lightweight mode (recommended for Apple Silicon)
   code_grasp info --lightweight
   ```

## Hardware Optimization Guide

### High-Performance Systems (16GB+ RAM, Dedicated GPU)
- Use standard mode for best embedding quality
- Increase batch size for faster processing: `--batch-size 8` or higher
- On NVIDIA GPUs, CUDA acceleration is used automatically
- For very large codebases, consider processing in chunks of 5,000-10,000 files

### Mid-Range Systems (8-16GB RAM)
- Standard mode should work with default batch size
- If experiencing memory issues, reduce batch size: `--batch-size 2`
- Process larger codebases in smaller chunks

### Memory-Constrained Systems (8GB RAM or less)
- Use lightweight mode: `--lightweight`
- Use minimal batch size: `--batch-size 1`
- Process smaller directories at a time (few hundred files max)

### Apple Silicon (M1/M2/M3)
- MPS acceleration is used automatically for improved performance
- The `info` command automatically uses lightweight mode on Apple Silicon to prevent segmentation faults
- 8GB RAM models: Use `--lightweight` mode for all commands with larger codebases
- 16GB+ RAM models: Standard mode should work well with default settings for most commands
- For optimal performance on 8GB models, use `--batch-size 2` with `--lightweight`

### NVIDIA GPU Systems
- CUDA acceleration is used automatically
- For GTX 1650-1660 class GPUs: Use standard settings but consider `--batch-size 2` for larger files
- For RTX 3000+ series: Can increase batch size to `8` or higher for better performance
- For GPUs with 8GB+ VRAM: Can use standard mode with large batch sizes

## Operating System Support

### macOS
- Tested on macOS Ventura+ with Apple Silicon
- Intel Macs should work with CPU acceleration
- MPS acceleration automatically used on M1/M2/M3

### Linux
- Works on major distributions (Ubuntu, Debian, CentOS, etc.)
- CUDA support for NVIDIA GPUs
- ROCm support for AMD GPUs may work but is untested

### Windows
- Should work on Windows 10/11 with proper Python environment
- CUDA support for NVIDIA GPUs
- Installation via WSL (Windows Subsystem for Linux) is recommended for best compatibility

## Supported Languages
- Python (.py)
- C++ (.cpp, .hpp, .h, .c)
- C# (.cs)
- Go (.go)
- Java (.java)
- Javascript (.js, .jsx)
- PHP (.php)
- Ruby (.rb)
- Typescript (.ts, .tsx)
- HTML (.html)
- CSS (.css)

## Memory Optimization

Code Grasp offers several memory optimization features:

1. **Lightweight Mode**: Use `--lightweight` to force using a smaller, more memory-efficient model
2. **Batch Processing**: Control the number of files processed at once with `--batch-size`
3. **Automatic Fallback**: If the large model fails to load, automatically falls back to a smaller model
4. **Half-Precision**: Uses float16 precision for the large model to reduce memory usage

## Known Limitations

- **Large Codebases**: May struggle with repositories containing tens of thousands of files
- **Memory Usage**: The Qodo-Embed model requires significant RAM/VRAM
- **Token Limits**: Individual files larger than 4,096 tokens will be truncated
- **Embedding Quality**: Lightweight mode provides lower quality embeddings than standard mode
- **Non-Text Files**: Binary files and non-supported text formats are skipped
- **File Encodings**: Assumes UTF-8 encoding for all files

## Troubleshooting

### Segmentation Faults
If you experience segmentation faults, try these solutions:

1. Use lightweight mode: `code_grasp --lightweight ...` (particularly important for the `info` command on Apple Silicon)
2. Reduce batch size: `code_grasp --batch-size 1 ...`
3. Process smaller directories at a time
4. Ensure you have at least 8GB of free RAM

**Note:** The `info` command now automatically uses lightweight mode on Apple Silicon to prevent segmentation faults.

### Performance Issues
For better performance:

1. On M1/M2 Macs, the tool automatically uses MPS acceleration
2. On systems with NVIDIA GPUs, CUDA will be used automatically
3. Increase batch size for faster processing if you have enough memory

### Installation Issues
If you encounter problems installing dependencies:

1. Ensure you have the latest pip: `pip install --upgrade pip`
2. On Windows, you may need Microsoft Visual C++ Build Tools
3. For CUDA support, ensure you have compatible CUDA drivers installed
4. For Apple Silicon, ensure you have Xcode command-line tools installed

## Contributing

Please see [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines on how to contribute to this project.

## Licensing

This project uses a dual licensing model:

1. **Code Grasp Code**: The Code Grasp tool itself is licensed under the **MIT License**, allowing for free use, modification, and distribution.

2. **Qodo-Embed-1-1.5B Model**: The embedding model used by this tool (Qodo-Embed-1-1.5B) is licensed under the **Qodo Open RAIL++-M License**, which:
   - Allows commercial and non-commercial use
   - Includes use-based restrictions to prevent harmful applications
   - Requires derivatives to retain these restrictions
   - Was released by QodoAI on February 19, 2025

When using Code Grasp, you must comply with both licenses - MIT for the code and Qodo Open RAIL++-M for the model. If you redistribute or create derivative works, you must include both license terms.

For the full Qodo Open RAIL++-M License text, please refer to [QodoAI's official website](https://www.qodo.ai/open-rail-m-license/).
