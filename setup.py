from setuptools import setup, find_packages


setup(
    name='Pyjo',
    version=__import__('Pyjo').__version__,
    description='Mojo clone in Python.',
    long_description=open('README.md').read(),
    author='Piotr Roszatycki',
    author_email='piotr.roszatycki@gmail.com',
    url='http://github.com/dex4er/Pyjo',
    download_url='https://github.com/dex4er/Pyjo/archive/master.zip',
    license='Artistic',
    include_package_data=True,
    zip_safe=True,
    keywords='django clean temporary cleanup pyc',
    packages=find_packages(),
    classifiers=[
        'Development Status :: 1 - Planning',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Artistic License',
        'Operating System :: POSIX',
        'Programming Language :: Python',
        'Framework :: Django',
        ],
    test_suite='test.TestSuite',
)
