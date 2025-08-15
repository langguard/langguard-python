"""Setup configuration for LangGuard."""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="langguard",
    version="0.0.1",
    author="Your Name",
    author_email="your.email@example.com",
    description="A Python library for language security",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/aprzy/langguard-python",
    packages=find_packages(where="src", exclude=["tests", "tests.*"]),
    package_dir={"": "src"},
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
    python_requires=">=3.11",
)