# -*- coding: utf-8 -*-
from setuptools import setup, find_packages

setup(
    name='firebase_idtoken',
    version='1.0.0',
    url='https://github.com/bobobobo/gae-firebase-idtoken',
    description='A simple python library for verifying Firebase ID tokens in Google App Engine',
    author='Bobo Häggström',
    author_email='bobo.haggstrom@gmail.com',
    license='MIT',
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2.7',
    ],
    keywords='firebase token verification gae appengine',
    py_modules=['firebase_idtoken']
)
