import pathlib
from setuptools import setup, find_packages

# Package meta-data.
NAME = "greenponik-waterpump-driver"
DESCRIPTION = "GreenPonik WaterPump i2c driver"
URL = "https://github.com/GreenPonik/GreenPonik_WaterPump_Driver"
EMAIL = "contact@greenponik.com"
AUTHOR = "GreenPonik SAS"
REQUIRES_PYTHON = ">=3.6.0"

# What packages are required for this module to be executed?
REQUIRED = [
    # 'requests', 'maya', 'records',
    "adafruit-blinka",
    "adafruit-extended-bus",
]

# What packages are optional?
EXTRAS = {
    # 'fancy feature': ['django'],
}

here = pathlib.Path(__file__).parent.resolve()

# Get the long description from the README file
long_description = (here / "README.md").read_text(encoding="utf-8")

# Load the package's version.py module as a dictionary.
# from version import __version__

setup(
    name=NAME,
    version="0.0.17",
    author=AUTHOR,
    author_email=EMAIL,
    description=DESCRIPTION,
    long_description=long_description,
    long_description_content_type="text/markdown",
    url=URL,
    license="MIT",
    install_requires=REQUIRED,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    packages=find_packages(exclude=("docs")),
    python_requires=REQUIRES_PYTHON,
    project_urls={  # Optional
        "Source": "https://github.com/GreenPonik/GreenPonik_WaterPump_Driver/",
        "Bug Reports": "https://github.com/GreenPonik/\
        GreenPonik_WaterPump_Driver/issues",
    },
    keywords="GreenPonik hydroponics WaterPump i2c driver \
         python hardware diy iot",
)
