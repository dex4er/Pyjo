#!/usr/bin/env python

from setuptools import setup, find_packages


setup(
    name='Pyjo',
    version='0.0.1',
    description='Mojo clone in Python.',
    long_description=''.join(open('README.md').readlines()[2:]),
    author='Piotr Roszatycki',
    author_email='piotr.roszatycki@gmail.com',
    url='http://github.com/dex4er/Pyjo',
    download_url='https://github.com/dex4er/Pyjo/archive/master.zip',
    license='Artistic',
    include_package_data=True,
    zip_safe=True,
    keywords='Mojo clone in Python - early dev stage',
    packages=find_packages(exclude=['t', 't.*']),
    classifiers=[
        'Development Status :: 1 - Planning',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Artistic License',
        'Operating System :: POSIX',
        'Programming Language :: Python',
        'Framework :: Pyjo',
    ],
    test_suite='test.TestSuite',
    install_requires=[
    ],
    extras_require={
        'regex': ['regex'],
    },
)
