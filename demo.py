#!/usr/bin/env python3
"""
Demo script for Code Grasp that showcases its capabilities.
This creates a simple project, embeds it, and asks questions about it.
"""
import os
import sys
import tempfile
import subprocess
import shutil
from pathlib import Path

# Simple Python file examples
PYTHON_CODE = {
    "sorting.py": """
def bubble_sort(arr):
    n = len(arr)
    for i in range(n):
        for j in range(0, n - i - 1):
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
    return arr

def quick_sort(arr):
    if len(arr) <= 1:
        return arr
    pivot = arr[len(arr) // 2]
    left = [x for x in arr if x < pivot]
    middle = [x for x in arr if x == pivot]
    right = [x for x in arr if x > pivot]
    return quick_sort(left) + middle + quick_sort(right)
""",
    "data_structures.py": """
class Node:
    def __init__(self, value):
        self.value = value
        self.next = None
        
class LinkedList:
    def __init__(self):
        self.head = None
        
    def append(self, value):
        if not self.head:
            self.head = Node(value)
            return
        
        current = self.head
        while current.next:
            current = current.next
        current.next = Node(value)
        
    def find(self, value):
        current = self.head
        while current:
            if current.value == value:
                return True
            current = current.next
        return False
""",
    "authentication.py": """
import hashlib
import os

def hash_password(password, salt=None):
    if salt is None:
        salt = os.urandom(32)
    
    hashed = hashlib.pbkdf2_hmac(
        'sha256',
        password.encode('utf-8'),
        salt,
        100000
    )
    
    return salt + hashed

def verify_password(stored_password, provided_password):
    salt = stored_password[:32]
    stored_hash = stored_password[32:]
    
    hash_check = hashlib.pbkdf2_hmac(
        'sha256',
        provided_password.encode('utf-8'),
        salt,
        100000
    )
    
    return hash_check == stored_hash

def login(username, password, user_database):
    if username not in user_database:
        return False
        
    stored_password = user_database[username]
    return verify_password(stored_password, password)
"""
}

# Simple JavaScript file examples
JAVASCRIPT_CODE = {
    "counter.js": """
class Counter {
    constructor(initialValue = 0) {
        this.count = initialValue;
    }
    
    increment() {
        this.count += 1;
        return this.count;
    }
    
    decrement() {
        this.count -= 1;
        return this.count;
    }
    
    reset() {
        this.count = 0;
        return this.count;
    }
}

module.exports = Counter;
""",
    "api.js": """
const express = require('express');
const app = express();
const port = 3000;

app.use(express.json());

const users = [
    { id: 1, name: 'John Doe', email: 'john@example.com' },
    { id: 2, name: 'Jane Smith', email: 'jane@example.com' }
];

app.get('/api/users', (req, res) => {
    res.json(users);
});

app.get('/api/users/:id', (req, res) => {
    const user = users.find(u => u.id === parseInt(req.params.id));
    if (!user) return res.status(404).json({ message: 'User not found' });
    res.json(user);
});

app.post('/api/users', (req, res) => {
    const newUser = {
        id: users.length + 1,
        name: req.body.name,
        email: req.body.email
    };
    users.push(newUser);
    res.status(201).json(newUser);
});

app.listen(port, () => {
    console.log(`API running on port ${port}`);
});
"""
}

def create_demo_project():
    """Create a temporary directory with sample code files."""
    project_dir = tempfile.mkdtemp(prefix="code_grasp_demo_")
    
    # Create Python files
    for filename, content in PYTHON_CODE.items():
        file_path = Path(project_dir) / filename
        with open(file_path, "w") as f:
            f.write(content)
    
    # Create JavaScript files
    for filename, content in JAVASCRIPT_CODE.items():
        file_path = Path(project_dir) / filename
        with open(file_path, "w") as f:
            f.write(content)
    
    return project_dir

def run_demo():
    """Run the demo script."""
    print("=== Code Grasp Demo ===")
    print("This demo will create a temporary project and showcase Code Grasp capabilities.")
    
    # Clear existing database files if they exist
    import os
    import shutil
    
    db_files = ["code_grasp.db", "code_grasp.faiss"]
    for file in db_files:
        if os.path.exists(file):
            try:
                os.remove(file)
                print(f"Removed existing database file: {file}")
            except Exception as e:
                print(f"Could not remove {file}: {e}")
    
    print("Creating demo project...")
    project_dir = create_demo_project()
    print(f"Created demo project at: {project_dir}")
    
    try:
        # Check if code_grasp is installed
        print("\nChecking Code Grasp installation...")
        try:
            subprocess.run(["code_grasp", "--help"], capture_output=True, check=True)
            print("Code Grasp is installed.")
        except (subprocess.CalledProcessError, FileNotFoundError):
            print("Code Grasp is not installed or not in PATH.")
            print("Please install Code Grasp with: pip install -e .")
            return
        
        # Run code_grasp commands
        print("\n1. Adding the demo project to Code Grasp")
        subprocess.run(["code_grasp", "add", "--lightweight", project_dir], check=True)
        
        print("\n2. Asking about sorting algorithms")
        subprocess.run(["code_grasp", "ask", "--lightweight", "How are sorting algorithms implemented?"], check=True)
        
        print("\n3. Asking about authentication")
        subprocess.run(["code_grasp", "ask", "--lightweight", "How is password hashing implemented?"], check=True)
        
        print("\n4. Analyzing the project directly")
        subprocess.run(["code_grasp", "ask-dir", "--lightweight", project_dir, "What REST API endpoints are available?"], check=True)
        
        print("\n5. Getting information about the database")
        subprocess.run(["code_grasp", "info", "--lightweight"], check=True)
        
    finally:
        # Clean up
        print("\nCleaning up demo project...")
        shutil.rmtree(project_dir)
        print("Demo completed.")

if __name__ == "__main__":
    run_demo()
