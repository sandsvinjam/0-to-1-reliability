"""
0-to-1 Reliability Framework
Build 99.9% reliability into your product from day one
"""

from setuptools import setup, find_packages
from pathlib import Path

# Read the README file
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(
    name="zero-to-one-reliability",
    version="1.0.0",
    author="Sandhya Vinjam",
    author_email="svinjam@example.com",
    description="Production-ready patterns for achieving 99.9% reliability in 0→1 products",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/sandsvinjam/0-to-1-reliability",
    project_urls={
        "Bug Tracker": "https://github.com/sandsvinjam/0-to-1-reliability/issues",
        "Documentation": "https://github.com/sandsvinjam/0-to-1-reliability/tree/main/docs",
        "Source Code": "https://github.com/sandsvinjam/0-to-1-reliability",
        "InfoQ Article": "https://www.infoq.com/",
        "Research Paper": "https://doi.org/10.36227/techrxiv.xxxxx",
    },
    packages=find_packages(exclude=["tests", "tests.*", "examples", "docs"]),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: System :: Monitoring",
        "Topic :: System :: Distributed Computing",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
    install_requires=[
        "prometheus-client>=0.19.0",
        "pyyaml>=6.0.1",
        "requests>=2.31.0",
        "python-dateutil>=2.8.2",
        "tenacity>=8.2.3",
        "circuitbreaker>=1.4.0",
        "python-json-logger>=2.0.7",
        "click>=8.1.7",
        "httpx>=0.26.0",
    ],
    extras_require={
        "dev": [
            "pytest>=7.4.4",
            "pytest-cov>=4.1.0",
            "pytest-mock>=3.12.0",
            "black>=23.12.1",
            "flake8>=7.0.0",
            "mypy>=1.8.0",
            "sphinx>=7.2.6",
        ],
        "datadog": ["datadog>=0.49.1"],
        "aws": ["boto3>=1.34.14"],
        "pagerduty": ["pypd>=1.1.0"],
        "testing": ["locust>=2.20.0"],
        "analysis": ["pandas>=2.1.4", "numpy>=1.26.2"],
    },
    entry_points={
        "console_scripts": [
            "reliability-init=tools.init:main",
            "reliability-analyze=tools.analysis.incident_analyzer:main",
            "reliability-chaos=tools.chaos.cli:main",
        ],
    },
    include_package_data=True,
    package_data={
        "patterns": ["config/*.yaml"],
        "dashboards": ["grafana/*.json", "datadog/*.json"],
        "playbooks": ["*.yaml", "*.md"],
    },
    zip_safe=False,
    keywords=[
        "reliability",
        "sre",
        "monitoring",
        "observability",
        "incident-management",
        "chaos-engineering",
        "circuit-breaker",
        "distributed-systems",
        "microservices",
        "0-to-1",
        "startup",
    ],
)
