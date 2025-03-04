# Changelog

## 0.1.0-alpha (2025-03-04)

> **⚠️ ALPHA RELEASE**: This tool is currently in alpha status and not production-ready. Use at your own risk.

Initial alpha release of Code Grasp.

### Features
- Integration with Qodo-Embed-1-1.5B embedding model
- Fallback to lightweight model (sentence-transformers/all-MiniLM-L6-v2)
- CLI commands for adding, querying, and analyzing code
- Support for multiple programming languages
- Memory-efficient processing options
- Automatic hardware acceleration detection (CUDA, MPS)

### Known Issues
- Limited error handling for edge cases
- Performance optimizations needed for very large repositories
- Documentation is preliminary

### Fixed Issues
- Fixed segmentation fault in `code_grasp info` command on M1/M2 Macs by defaulting to lightweight model

### Hardware Requirements
- Minimum: 8GB RAM, modern CPU
- Recommended: 16GB RAM, GPU with 4GB+ VRAM
- For large codebases: 32GB RAM, GPU with 8GB+ VRAM

### Next Steps
- Improved memory efficiency
- Better error handling
- Additional language support
- Integration with code search tools
- Support for analyzing code snippets
- Distributed processing for very large codebases
