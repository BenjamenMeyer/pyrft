# -*- coding: utf-8 -*-*

try:
    from distutils.core import setup
except ImportError:
    from ez_setup import use_setuptools
    use_setuptools()
    from setuptools import setup
finally:
    from setuptools import find_packages

long_description = """PyRTF is an FTP replacement with the ability to do fast,
reliable file transfer operations. It may be used as an
API embeddable into other applications, or with its own
client (pyrft) and server (pyrftd) applications, both
to be provided as at least refernce applications.
"""

REQUIRES = [
]

TEST_REQUIRES = [
    'coverage',
    'ddt',
    'mock',
    'nose',
    'nose-exclude',
    'pep8',
    'setuptools>=1.1.6',
    'testtools',
    'testfixtures',
]


# TODO: Add download_url = github repository
# TODO: Add install_requires=[]
setup(name='PyRFT',
      version='0.1',
      url='github.com/ClockwerksSoftware/pyrft',
      author='Clockwerks Software, LLC',
      author_email='bmeyer@clockwerkssoftware.net',
      maintainer='Benjamen R. Meyer',
      maintainer_email='bmeyer@clockwerkssoftware.net',
      description='Python Reliable File Transfer',
      long_description=long_description,
      classifiers=['Development Status :: 4 - Beta',
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
      zip_safe=False,
      packages=find_packages(exclude=['tests']),
      include_package_data=True,

      install_requires=REQUIRES,

      tests_require=TEST_REQUIRES,
      test_suite='pyrft',
      )
