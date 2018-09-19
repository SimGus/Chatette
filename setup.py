from os.path import dirname, join

from setuptools import find_packages, setup

# Manual:
# https://the-hitchhikers-guide-to-packaging.readthedocs.io/en/latest/quickstart.html

setup(
    name="chatette",
    version="1.2.0",
    description="A dataset generator for Rasa NLU",
    author="SimGus",
    license="MIT",
    url="https://github.com/SimGus/Chatette",
    packages=find_packages(),
    long_description=open(join(dirname(__file__), "README.md")).read(),
    long_description_content_type="text/markdown",
    classifiers=[
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ]
)
