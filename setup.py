# for --editable flag option
from setuptools import setup

# read the contents of your README file
from pathlib import Path
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(
    name="ipydoodle",
    version="0.1.1",
    # use the code below to enable extensions automatically
    install_requires=[
        'ipycanvas==0.12.0'
    ],
    packages=['ipydoodle'],
    long_description=long_description,
    long_description_content_type='text/markdown'
)
