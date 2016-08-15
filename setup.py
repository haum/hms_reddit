from setuptools import setup

from os import path

here = path.abspath(path.dirname(__file__))
with open(path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()



setup(
    name='hms_reddit',
    version='2.1',
    packages=['hms_reddit', 'hms_reddit.tests'],
    scripts=['bin/hms_reddit'],

    url='https://github.com/haum/hms_reddit',
    license='MIT',

    author='Romain Porte (MicroJoe)',
    author_email='microjoe@microjoe.org',

    description='HAUM\'s Reddit microservice',
    long_description=long_description,

    classifiers = [
        'Development Status :: 3 - Alpha',

        'Intended Audience :: Developers',

        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],

    install_requires=['pika', 'hms_base>=2.0,<3', 'irc', 'coloredlogs', 'praw'],

    test_suite='nose.collector',
    tests_require=['nose'],
)
