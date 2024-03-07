"""The setup module."""

import os

from setuptools import find_packages, setup

# variable that we set as the version of the library, this is done for easier extraction from the
# actions pipeline.
VERSION: str = "1.1.0"

# get the current path
CURRENT_PATH = os.path.dirname(os.path.abspath(__file__))
# construct the readme path
README_PATH = os.path.join(os.path.join(CURRENT_PATH, "docs"), "README.rst")
# now construct the requirements path
REQS_PATH = os.path.join(CURRENT_PATH, "requirements_prod.txt")

# parse the readme into a variable
with open(README_PATH, "r", encoding="utf8") as rmd:
    long_desc = rmd.read()

# fetch the requirements required
with open(REQS_PATH, "r", encoding="utf8") as req_file:
    requirements = req_file.read().split("\n")


if __name__ == "__main__":
    setup(
        name="quibraries",
        version=VERSION,
        author="Andreas A. Grammenos",
        author_email="axorl@quine.sh",
        description="A thread-safe Python wrapper for the libraries.io API",
        long_description=long_desc,
        long_description_content_type="text/x-rst",
        url="https://github.com/andylamp/quibraries/",
        packages=find_packages(),
        install_requires=requirements,
        classifiers=[
            "Development Status :: 5 - Production/Stable",
            "Programming Language :: Python :: 3.10",
            "Programming Language :: Python :: 3.11",
            "Programming Language :: Python :: 3.12",
            "License :: OSI Approved :: MIT License",
        ],
        license="MIT",
        license_files=("LICENSE",),
        python_requires=">=3.10",
        include_package_data=True,
        zip_safe=False,
    )
