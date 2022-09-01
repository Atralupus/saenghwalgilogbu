from setuptools import setup, find_packages

setup(
    name="saenghwalgilogbu",
    version="0.1.0",
    description="saenghwalgilogbu",
    author="Atralupus",
    author_email="me@atralupus.com",
    packages=find_packages(
        where=".",
        include=["saenghwalgilogbu*"],
        exclude=["tests"],
    ),
    python_requires=">=3.6",
    install_requires=[
        "typer[all]~=0.6.1",
    ],
    classifiers=[
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
    ],
)
