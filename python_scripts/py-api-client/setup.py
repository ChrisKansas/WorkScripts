from setuptools import setup, find_namespace_packages

setup(
    name="Client",
    version="1.27.0",
    description="ThreatX API Python Client",
    packages=find_namespace_packages(include=['client.*']),
    install_requires=[
        'furl',
        'pymongo',
        'requests'
    ]
)
