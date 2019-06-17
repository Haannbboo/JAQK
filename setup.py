import setuptools
import os
import codecs

with open("README.md", "r") as fh:
    long_description = fh.read()

def read(fname):
    return codecs.open(os.path.join(os.path.dirname(__file__), fname)).read()

def install_requirements():
    reqs = [
        'pandas>=0.21.0',
        'requests>=2.1.0',
        'numpy>=1.14.0',
        'pyquery>=1.4.0',
        'aiohttp>=3.4.0',
        'PySimpleGUI>=3.0.0',
        'scipy>=1.0.0'
        ]
    return reqs
        
        

setuptools.setup(
    name="JAQK",
    version=read('VERSION.txt'),
    author="Hanbo Guo",
    author_email="hbopublic@163.com",
    description="A light toolkit for crawling financia data and basic analysis and calcualtions.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    license='MIT',
    url="https://github.com/Haannbboo/JAQK",
    install_requires=install_requirements(),
    keywords='US Stock Market Data',
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3.3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "License :: OSI Approved :: MIT License",
    ],
)

