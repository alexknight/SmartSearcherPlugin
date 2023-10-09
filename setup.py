from setuptools import setup, find_packages

setup(
    name='SmartSearcherPlugin',
    version='0.1',
    packages=find_packages(),
    install_requires=[
        'requests',
        'bs4',
        'redis',
        'scikit-learn'
    ],
)
