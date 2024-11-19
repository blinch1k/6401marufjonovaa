from setuptools import setup

setup(
    name = 'stocks_analyzer',
    version = '0.1',
    description = 'Package for analyze time series',
    author = 'Marufjonov Abdubasir',
    author_email = 'energizer2111@gmail.com',
    packages = ['stocks_analyzer'],
    install_requires = ['numpy', 'pandas', 'scipy'],
)