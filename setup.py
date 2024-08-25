from setuptools import setup, find_packages

setup(
    name="automated_test_framework",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        "requests",
        "pytest",
    ],
)