# setup.py

from setuptools import find_packages, setup

setup(
    name="config_manager",
    version="0.1.0",
    description="A modular configuration management system supporting multiple formats.",
    author="Will Morris",
    author_email="willmorris188@gmail.com",
    packages=find_packages(),
    install_requires=["psycopg2-binary>=2.9", "PyYAML>=6.0", "python-dotenv>=1.0"],
    python_requires=">=3.7",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
)
