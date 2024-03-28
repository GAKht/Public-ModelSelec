"""
                            This script includes metadata about the modelselec package
                                and the instructions for how to install it

                                            Guillaume A. Khayat
                                           guill.khayat@gmail.com
                                                2024-02-16
"""
from setuptools import setup

with open('requirements.txt') as f:
    requirements = f.read().splitlines()

setup(
    name='modelselec',
    version='2.0.0',
    packages=['modelselec', 'modelselec.db', 'modelselec.eda', 'modelselec.util'],
    author='Guillaume A. Khayat',
    author_email='guill.khayat@gmail.com',
    description='The modelselec package is designed to facilitate model development and selection',
    url='https://github.com/GAKht/Public-ModelSelec',
    install_requires=requirements,
)
