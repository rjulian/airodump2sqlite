from setuptools import setup, find_packages

setup(
    name='airodump2sqlite',
    version='0.0.4',
    author='Richard Julian',
    author_email='richard@rjulian.net',
    packages=find_packages(),
    scripts=['bin/airodump2sqlite'],
    license='LICENSE.txt',
    description='Parse airodump data and store in a queriable format.',
    long_description=open('README.md').read(),
    install_requires=[
        "names == 0.3.0"
    ],
)
