from setuptools import setup, find_packages

setup(
    name='whoiswalkingby',
    version='0.0.3',
    author='Richard Julian',
    author_email='richard@rjulian.net',
    packages=find_packages(),
    url='http://pypi.python.org/pypi/TowelStuff/',
    scripts=['bin/whoiswalkingby'],
    license='LICENSE.txt',
    description='Parse airodump data and store in a queriable format.',
    long_description=open('README.md').read(),
    install_requires=[
        "names == 0.3.0"
    ],
)
