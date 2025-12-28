from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="pyguard-args",
    version="0.1.1",
    packages=find_packages(),
    author="Mateusz Jasinski",
    author_email="mateusz@jasinski.software",
    description="A Python library for validating function arguments using decorators",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/tadow-dev/pyguard",
    license="MIT",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
    keywords="validation decorator arguments type-checking",
    python_requires=">=3.10",
)
