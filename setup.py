#!/usr/bin/env python

from distutils.core import setup
import setuptools

long_description = """PyRTF is an FTP replacement with the ability to do fast,
reliable file transfer operations. It may be used as an
API embeddable into other applications, or with its own
client (pyrtf) and server (pyrftd) applications, both
to be provided as at least refernce applications.
"""

#TODO: Add url = github repository
#TODO: Add download_url = github repository
#TODO: Add install_requires=[]
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
	scripts=[
		'bin/pyrtf',
		'bin/pyrtf-config',
		'sbin/pyrtfd',
		'sbin/pyrtfd-config',
		],
	packages=['pyrtf'],
	package_dir={'pyrtf': 'pyrft'},
	data_files=[
		('scripts', ['scripts/pyrftd'] ),
		('config', ['configs/user.conf', 'configs/system.conf'])
		],
	setup_requires=['nose>=1.0']
	)

