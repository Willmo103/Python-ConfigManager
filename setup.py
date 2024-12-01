# setup.py

from setuptools import find_packages, setup

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="config_manager",
    version="0.1.0",
    description="A modular configuration management system supporting multiple formats.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Will Morris",
    author_email="willmorris188@gmail.com",
    url="https://git.willmo.dev/willmo103/Python-ConfigManager",
    packages=find_packages(),
    include_package_data=True,  # Include files from MANIFEST.in
    install_requires=[
        "psycopg2-binary>=2.9",
        "PyYAML>=6.0",
        "python-dotenv>=1.0",
    ],
    extras_require={
        "dev": [
            "black==24.10.0",
            "isort==6.0.0b2",
            "pytest==8.3.3",
            "pytest-cov==6.0.0",
            "pytest-mock==3.14.0",
        ],
    },
    python_requires=">=3.7",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
        "License :: OSI Approved :: MIT License",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries",
    ],
    keywords="configuration management json yaml env sqlite postgres",
)
