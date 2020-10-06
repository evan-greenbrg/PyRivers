from setuptools import setup

setup(
    name='PyRivers',
    version='0.1.0',
    author='Evan Greenberg',
    author_email='',
    packages=['PyRivers'],
    license='LICENSE.txt',
    description='Helper functions to perform kinematic analysis on rivers',
    long_description=open('README.txt').read(),
    install_requires=[
        "numpy",
        "pandas",
        "rasterio"
    ],
)
