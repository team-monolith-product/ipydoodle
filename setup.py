# for --editable flag option
from setuptools import setup

setup(
    name="ipydoodle",
    version="0.0.1",
    # use the code below to enable extensions automatically
    data_files=[
        ("etc/ipython/", [
            "ipython-config/ipython_config.py"
        ])
    ],
    packages=['ipydoodle'],
)