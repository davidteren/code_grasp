# Code Grasp Usage Examples

This document provides practical examples of how to use Code Grasp for various scenarios.

> **⚠️ ALPHA RELEASE**: This tool is currently in alpha status and not production-ready. Use at your own risk.

## Basic Usage Examples

### Adding a Code Repository

```bash
# Add a small to medium repository
code_grasp add ~/projects/my-python-app

# Add a large repository with reduced batch size for memory efficiency
code_grasp add --batch-size 2 ~/projects/large-codebase

# Use lightweight mode for memory-constrained systems
code_grasp add --lightweight ~/projects/my-project
```

### Querying About Code

```bash
# Ask a general coding question
code_grasp ask "How to implement a doubly linked list?"

# Ask about a specific programming technique
code_grasp ask "What are different ways to handle error cases in Ruby?"

# Ask about a design pattern
code_grasp ask "How to implement the observer pattern?"
```

### Analyzing a Specific Directory

```bash
# Ask about a directory's code without adding it to the database
code_grasp ask_dir ~/projects/my-app/src "How is authentication handled?"

# Analyze using lightweight mode
code_grasp ask_dir --lightweight ~/projects/web-app "What API endpoints are implemented?"

# Focus on a specific subdirectory
code_grasp ask_dir ~/projects/app/controllers "How is error handling implemented?"
```

### Getting Information About the Database

```bash
# Display system information and database statistics
code_grasp info
```

## Advanced Usage Examples

### Processing Different Language Codebases

```bash
# Python project
code_grasp add ~/projects/python-backend

# JavaScript/TypeScript project
code_grasp add ~/projects/react-frontend

# Mixed language project
code_grasp add ~/projects/full-stack-app
```

### Querying Specific Aspects of Code

```bash
# Finding security-related code
code_grasp ask "How is password hashing implemented?"

# Understanding data flow
code_grasp ask_dir ~/projects/app "How does data flow from the API to the database?"

# Identifying design patterns
code_grasp ask "Where is the factory pattern used in this codebase?"
```

### Memory-Optimized Processing for Large Codebases

```bash
# Process a large codebase in chunks
code_grasp add --batch-size 2 ~/projects/large-app/src/module1
code_grasp add --batch-size 2 ~/projects/large-app/src/module2
code_grasp add --batch-size 2 ~/projects/large-app/src/module3

# Using lightweight mode for the initial scan
code_grasp add --lightweight ~/projects/large-app
```

## Specific Use Cases

### Code Review Assistance

```bash
# Understand new code additions
code_grasp ask_dir ~/projects/feature-branch "What changed compared to the base functionality?"

# Find potential issues
code_grasp ask_dir ~/projects/pull-request "Are there any potential memory leaks or performance issues?"
```

### Architecture Understanding

```bash
# Get overview of project structure
code_grasp ask "What are the main components and how do they interact?"

# Understand dependency relationships
code_grasp ask "What are the key dependencies between modules?"
```

### Learning a New Codebase

```bash
# First, add the repository
code_grasp add ~/projects/new-codebase

# Then ask questions to understand it
code_grasp ask "What's the entry point of this application?"
code_grasp ask "How is the database accessed in this codebase?"
code_grasp ask "What is the authentication flow?"
```

### Processing a Monorepo

```bash
# Process the entire monorepo (may require high memory)
code_grasp add ~/projects/monorepo

# Or process individual packages
code_grasp add ~/projects/monorepo/packages/frontend
code_grasp add ~/projects/monorepo/packages/backend
code_grasp add ~/projects/monorepo/packages/common

# Then ask questions about the whole architecture
code_grasp ask "How do the frontend and backend communicate?"
```

## Hardware-Optimized Examples

### High-Performance Systems

```bash
# Process large codebases with high batch size
code_grasp add --batch-size 16 ~/projects/large-codebase

# Query with complex questions
code_grasp ask "Explain the entire authorization flow from login to accessing protected resources"
```

### Memory-Constrained Systems

```bash
# Use all memory optimizations
code_grasp add --lightweight --batch-size 1 ~/projects/small-project

# Process large codebases directory by directory
code_grasp add --lightweight --batch-size 1 ~/projects/large-app/src/feature1
code_grasp add --lightweight --batch-size 1 ~/projects/large-app/src/feature2
```

### GPU-Optimized Usage

```bash
# On systems with NVIDIA GPUs, CUDA is used automatically
# You can increase batch size for better utilization
code_grasp add --batch-size 8 ~/projects/large-codebase

# For very powerful GPUs, can go even higher
code_grasp add --batch-size 16 ~/projects/huge-monorepo
```