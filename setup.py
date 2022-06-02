# for --editable flag option
from setuptools import setup

setup(
    name="ipydoodle",
    version="0.2.0",
    # use the code below to enable extensions automatically
    install_requires=[
        'ipycanvas==0.12.0',
        'jupyter_ui_poll'
    ],
    packages=['ipydoodle'],
)