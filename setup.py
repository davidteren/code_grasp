from setuptools import setup, find_packages

setup(
    name="code_grasp",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "click",
        "transformers",
        "torch",
        "faiss-cpu",
        "numpy",
        # flash_attn is optional and may cause installation issues
        # "flash_attn",
    ],
    extras_require={
        "full": ["flash_attn"],
    },
    entry_points={
        "console_scripts": [
            "code_grasp = code_grasp.cli:cli",
        ],
    },
    author="David Teren",
    description="A CLI to analyze code with Qodo-Embed-1",
)