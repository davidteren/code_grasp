# Contributing to Code Grasp

Thank you for your interest in contributing to Code Grasp! This document provides guidelines and workflows for contributing to the project.

## Branching Strategy

This project follows a simplified git-flow branching model:

- `main`: Contains the stable, released versions of Code Grasp
- `develop`: Active development branch where all feature branches get merged
- `feature/*`: Feature branches created from `develop` for specific features or improvements
- `bugfix/*`: Bugfix branches created from `develop` for specific bug fixes
- `release/*`: Temporary branches for release preparation

## Development Workflow

1. **Fork the repository** (if you're not a core contributor)
2. **Create a branch** from `develop`:
   ```bash
   git checkout develop
   git pull origin develop
   git checkout -b feature/your-feature-name
   ```
3. **Make your changes** and commit them with clear, descriptive messages
4. **Test your changes** thoroughly
5. **Submit a pull request** to the `develop` branch

## Code Style

- Follow PEP 8 guidelines for Python code
- Use descriptive variable names
- Add comments for complex logic
- Include docstrings for functions and classes

## Testing

Before submitting a pull request, ensure:

1. Your code works as expected
2. All existing functionality still works
3. Edge cases are handled appropriately
4. Performance implications are considered

## Pull Request Process

1. Update the README.md or documentation with details of changes if appropriate
2. Update the CHANGELOG.md with a description of your changes
3. Submit the pull request to the `develop` branch
4. Address any feedback from code reviewers

## Development Environment Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/code_grasp.git
   cd code_grasp
   ```

2. Create and activate a virtual environment:
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install development dependencies:
   ```bash
   pip install torch
   pip install -e .
   pip install pytest pytest-cov flake8 black
   ```

## Adding New Features

When adding new features:

1. Consider memory efficiency and performance
2. Ensure backwards compatibility where possible
3. Add appropriate error handling
4. Document the feature in the code and in user documentation

## Current Development Priorities

1. Improving memory efficiency for large codebases
2. Adding support for more programming languages
3. Enhancing query capabilities
4. Performance optimizations
5. Better error handling and reporting

## License

By contributing to Code Grasp, you agree that your contributions will be licensed under the project's MIT License.