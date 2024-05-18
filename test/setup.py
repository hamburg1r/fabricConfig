#!/usr/bin/env python

from setuptools import setup, find_packages

setup(
	name='bar',
	version='1.0',
	# Modules to import from other scripts:
	packages=find_packages(),
	package_data = {
		"": ['assets/*']
		# 'desktop.bar': ['assets/*']
	},
)
