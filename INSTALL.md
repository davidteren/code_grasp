# Installation Guide for Code Grasp

This guide provides detailed installation instructions for different operating systems and hardware configurations.

> **⚠️ ALPHA RELEASE**: This tool is currently in alpha status and not production-ready. Use at your own risk.

## Prerequisites

- Python 3.8 or higher
- pip (package installer for Python)
- Git (optional, for cloning the repository)
- Virtual environment capability (venv, conda, etc.)

## Basic Installation

### 1. Clone or download the repository
```bash
git clone https://github.com/your-username/code_grasp.git
cd code_grasp
```

### 2. Create and activate a virtual environment
```bash
# Using venv (recommended)
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install PyTorch

PyTorch installation varies by system. Install the appropriate version for your hardware:

```bash
# CPU-only version
pip install torch

# For CUDA support (NVIDIA GPUs)
pip install torch --index-url https://download.pytorch.org/whl/cu118  # For CUDA 11.8
```

For detailed PyTorch installation instructions based on your hardware, see: https://pytorch.org/get-started/locally/

### 4. Install other dependencies and the package
```bash
pip install -r requirements.txt
pip install -e .
```

## Platform-Specific Instructions

### macOS (Apple Silicon - M1/M2/M3)

```bash
# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install PyTorch with MPS support
pip install torch

# Install other dependencies and the package
pip install -r requirements.txt
pip install -e .
```

Notes:
- MPS (Metal Performance Shaders) acceleration is used automatically.
- Make sure you have Xcode Command Line Tools installed: `xcode-select --install`
- If you have 8GB RAM, consider using lightweight mode for larger codebases.

### macOS (Intel)

```bash
# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install PyTorch
pip install torch

# Install other dependencies and the package
pip install -r requirements.txt
pip install -e .
```

### Linux (with NVIDIA GPU)

```bash
# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install PyTorch with CUDA support (choose appropriate CUDA version)
pip install torch --index-url https://download.pytorch.org/whl/cu118  # For CUDA 11.8

# Install other dependencies and the package
pip install -r requirements.txt
pip install -e .
```

Notes:
- Ensure you have compatible NVIDIA drivers installed
- Check your CUDA version with `nvidia-smi`
- Choose the appropriate PyTorch CUDA version based on your installed CUDA

### Linux (CPU only)

```bash
# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install PyTorch CPU version
pip install torch --index-url https://download.pytorch.org/whl/cpu

# Install other dependencies and the package
pip install -r requirements.txt
pip install -e .
```

### Windows

```bash
# Create virtual environment
python -m venv venv
venv\Scripts\activate

# Install PyTorch (with or without CUDA)
pip install torch  # CPU only
# or for CUDA:
pip install torch --index-url https://download.pytorch.org/whl/cu118  # For CUDA 11.8

# Install other dependencies and the package
pip install -r requirements.txt
pip install -e .
```

Notes:
- You may need Microsoft Visual C++ Build Tools for some packages
- Windows users might find installation easier through WSL (Windows Subsystem for Linux)

## Installation via WSL (Windows Subsystem for Linux)

```bash
# Install and setup WSL if not already done
# Then, in your WSL terminal:

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies as per Linux instructions above
```

## Verify Installation

After installation, verify that Code Grasp works correctly:

```bash
code_grasp info
```

This should show information about the available models and system configuration.

## Troubleshooting Installation Issues

### Common Issues

1. **PyTorch installation fails**:
   - Make sure you're using a compatible Python version (3.8-3.11 recommended)
   - Try installing PyTorch separately before other dependencies
   - Check the PyTorch website for the latest installation instructions

2. **CUDA not found**:
   - Verify NVIDIA drivers are installed: `nvidia-smi`
   - Ensure CUDA toolkit is installed and in your PATH
   - Check that PyTorch was installed with CUDA support: `python -c "import torch; print(torch.cuda.is_available())"`

3. **Model download issues**:
   - Ensure you have a good internet connection
   - Temporary HuggingFace server issues: try again later
   - Check your disk space: the models require several GB of storage

4. **Segmentation faults during model loading**:
   - This is typically a memory issue
   - Try using `--lightweight` mode
   - Increase your system's swap space

5. **Package conflicts**:
   - Use a fresh virtual environment
   - Update pip: `pip install --upgrade pip`
   - Install packages one by one to identify conflicts