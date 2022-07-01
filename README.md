# Python Package: tgdhstruct
This repo contains the source code and source distribution for **tgdhstruct**, a Python library that provides a tree structure to implement a Tree-based Group Diffie-Hellman (TGDH) encryption scheme. 
## Installation
Download the source distribution (`<filename>.tar.gz`) from within the `dist` directory.

Install Graphviz:

***MacOS***
```
brew install graphviz
```
***Linux***
```
sudo apt install graphviz
```
Use pip3 to install:
```
pip3 install <filename>.tar.gz
```
## Building Source Distribution
The source distribution file (sdist) can be built using the following command:
```
python3 setup.py sdist --formats=gztar
```
