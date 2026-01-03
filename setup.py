from setuptools import setup, find_packages

# Read README for long description
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="pyportable-installer",
    version="0.1.0",
    author="David Silva",
    author_email="david.emery.silva@gmail.com",
    description="A CLI tool to download and configure Portable Python (Embedded) automatically.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/your-username/your-repo",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: Microsoft :: Windows",
    ],
    python_requires=">=3.8",
    install_requires=[
        "requests>=2.0.0",
        "rich>=10.0.0",
    ],
    entry_points={
        "console_scripts": [
            "pyportable=pyportable_installer.cli:main",
        ],
    },
    include_package_data=True,
)