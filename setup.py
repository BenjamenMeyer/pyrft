#!/usr/bin/env python

from distutils.core import setup

with open('README.rst') as ld_input:
	long_description = ld_input.read()

#TODO: Add url = github repository
#TODO: Add download_url = github repository
setup(name='PyRFT',
      version='1.0',
	  author='Benjamen R. Meyer',
	  author_email='bm_witness@yahoo.com',
	  maintainer='Benjamen R. Meyer',
	  maintainer_email='bm_witness@yahoo.com',
	  description='Python Reliable File Transfer',
	  long_description=long_description,
	  classifiers=[
		'Development Status :: 4 - Beta',
		'Environment :: Console', 
		'Environment :: Web Environment',
		'Intended Audience :: End Users',
		'Intended Audience :: Developers',
		'Intended Audience :: System Administrators',
		'License :: OSI Approved :: Apache License Version 2',
		'Operating System :: Microsoft :: Windows',
		'Operating System :: POSIX',
		'Programming Language :: Python',
		'Topic :: Communication :: File Transfer',
		'Topic :: Network :: File Transfer',
		'Topic :: Programming :: Python',
		'Topic :: API :: JSON'
		],
	  platforms=[
		'linux',

