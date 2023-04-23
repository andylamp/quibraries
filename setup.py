"""The setup module."""
import os

from setuptools import find_packages, setup

# get the current path
CURRENT_PATH = os.path.dirname(os.path.abspath(__file__))

# parse the readme into a variable
with open("docs/README.rst", "r", encoding="utf8") as rmd:
    long_desc = rmd.read()

# fetch the requirements required
with open(os.path.join(CURRENT_PATH, "requirements_prod.txt"), "r", encoding="utf8") as req_file:
    requirements = req_file.read().split("\n")


if __name__ == "__main__":
    setup(
        name="quibraries",
        version="0.0.4",
        author="Andreas A. Grammenos",
        author_email="axorl@quine.sh",
        description="A thread-safe Python wrapper for the libraries.io API",
        long_description=long_desc,
        url="https://github.com/andylamp/quibraries/",
        packages=find_packages(),
        install_requires=requirements,
        classifiers=[
            "Development Status :: 4 - Beta",
            "Programming Language :: Python :: 3.9",
            "Programming Language :: Python :: 3.10",
            "Programming Language :: Python :: 3.11",
            "License :: OSI Approved :: MIT License",
        ],
        license="MIT",
        license_files=("LICENSE",),
        python_requires=">=3.9",
        include_package_data=True,
        zip_safe=False,
    )
