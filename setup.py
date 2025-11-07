from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="cgpa-co-po-analysis",
    version="1.0.0",
    author="Academic Analytics Team",
    author_email="fahmidafaiza918@gmail.com",
    description="Comprehensive CGPA and CO/PO Analysis System with ML",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/username/cgpa-co-po-analysis",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Education",
        "Topic :: Education",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
    install_requires=requirements,
    include_package_data=True,
    package_data={
        "": ["*.md", "*.txt", "*.toml"],
    },
    entry_points={
        "console_scripts": [
            "cgpa-system=app:main",
        ],
    },
)