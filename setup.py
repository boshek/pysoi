from setuptools import setup, find_packages

setup(
    name="pysoi",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "pandas>=1.0.0",
        "requests>=2.24.0",
        "numpy>=1.19.0",
    ],
    author="Sam Albers",
    author_email="sam.albers@gmail.com",
    description="Import Various Northern and Southern Hemisphere Climate Indices",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/boshek/pysoi",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
