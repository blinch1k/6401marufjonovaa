from setuptools import setup

setup(
    name = 'stocks_analyzer',
    version = '0.1',
    description = 'Package for analyze time series',
    author = 'Abeldinov Rafael',
    author_email = 'raf2003@bk.ru',
    packages = ['stocks_analyzer'],
    install_requires = ['numpy', 'pandas', 'scipy'],
)