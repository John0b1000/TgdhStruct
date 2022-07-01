from setuptools import setup, find_packages

from src import binary_tree

setup(
    name='tgdhstruct',
    version='1.0.0',
    packages=find_packages(),
    url='https://github.com/John0b1000/tgdhstruct',
    author='John Nori',
    author_email='johnlnori8@gmail.com',
    description='tgdh structure library',
    setup_requires=['anytree'],
    install_requires=['anytree']
)
