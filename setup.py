from os.path import dirname, join

from setuptools import find_packages, setup

# Manual:
# https://the-hitchhikers-guide-to-packaging.readthedocs.io/en/latest/quickstart.html

setup(
    name='chatette',
    version='1.1.5',
    packages=find_packages(),
    long_description=open(join(dirname(__file__), 'README.md')).read(),
)
