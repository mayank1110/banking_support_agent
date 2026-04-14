"""
Setup script for Banking Customer Support AI Agent
"""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="banking-support-agent",
    version="1.0.0",
    author="Mayank",
    author_email="mayank.jha10@gmail.com",
    description="An intelligent AI-powered customer support agent for banking institutions using LangGraph and Hugging Face Transformers",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/mayank1110/banking_support_agent",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Framework :: LangChain",
        "Topic :: Office/Business :: Financial :: Banking",
    ],
    python_requires=">=3.8",
    install_requires=requirements,
    entry_points={
        "console_scripts": [
            "banking-agent=src.ui:launch_ui",
        ],
    },
    include_package_data=True,
    package_data={
        "banking_support_agent": ["data/*.csv", "models/*"],
    },
)
