#!/usr/bin/env python

from setuptools import setup

setup(
name='django-liveresource',
version='0.0.1',
description='Django LiveResource library',
author='Justin Karneges',
author_email='justin@fanout.io',
url='https://github.com/fanout/django-liveresource',
license='MIT',
packages=['django_liveresource'],
install_requires=['django-grip>=1.1.0'],
classifiers=[
	'Topic :: Utilities',
	'License :: OSI Approved :: MIT License'
]
)
