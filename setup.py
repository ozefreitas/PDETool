import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="PDETool",
    version="1.0.0",
    author="José Freitas",
    author_email="jpsfreitas12@gmail.com",
    description="Package for plastic degrading enzymes prediction from metagenomic samples",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/pg42872/PDETool",
    packages=setuptools.find_packages(),
    classifiers=(
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ),
)
