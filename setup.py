#!/usr/bin/env python

from setuptools import setup, find_packages


setup(
    name='Pyjoyment',
    version='0.0.1',
    description='Mojolicious clone in Python.',
    long_description=''.join(open('README.md').readlines()[2:]),
    author='Piotr Roszatycki',
    author_email='piotr.roszatycki@gmail.com',
    url='http://github.com/dex4er/Pyjoyment',
    download_url='https://github.com/dex4er/Pyjoyment/archive/master.zip',
    license='Artistic',
    include_package_data=True,
    zip_safe=True,
    keywords='mojo mojolicious pyjo pyjoyment framework http html async',
    packages=find_packages(exclude=['t', 't.*']),
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Artistic License',
        'Operating System :: POSIX',
        'Programming Language :: Python',
        'Framework :: Pyjoyment',
    ],
    test_suite='test.TestSuite',
    install_requires=[
    ],
    extras_require={
    },
)
