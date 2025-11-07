"""
sh0rtifier Setup
"""

from pathlib import Path

from setuptools import find_packages, setup

# Read README for long description
readme_file = Path(__file__).parent / "README.md"
long_description = readme_file.read_text(encoding="utf-8") if readme_file.exists() else ""

setup(
    name="sh0rtifier",
    version="1.0.0",
    author="sl0thm4n",
    author_email="thesl0thm4n@gmail.com",
    description="Convert 16:9 videos to YouTube Shorts format (9:16)",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/sl0thm4n/sh0rtifier",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: End Users/Desktop",
        "Topic :: Multimedia :: Video :: Conversion",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.9",
    install_requires=[
        "moviepy>=1.0.3",
        "opencv-python>=4.8.0",
        "numpy>=1.24.0",
        "tqdm>=4.65.0",
    ],
    extras_require={
        "dev": [
            "pytest>=7.4.0",
            "pytest-cov>=4.1.0",
            "black>=23.0.0",
            "flake8>=6.0.0",
            "pyinstaller>=5.13.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "sh0rtifier=cli:main",
            "sh0rtifier-gui=gui:main",
        ],
    },
    keywords="youtube shorts video converter 16:9 9:16 sh0rtifier",
    project_urls={
        "Bug Reports": "https://github.com/sl0thm4n/sh0rtifier/issues",
        "Source": "https://github.com/sl0thm4n/sh0rtifier",
    },
)
