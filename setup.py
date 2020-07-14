import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="fefiphopy", # Replace with your own username
    version="0.0.3",
    author="Nicholas Worley",
    author_email="nworley01@yahoo.com",
    description="A package for cleaning and analyzing fiber photomertry data.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/nworley01/fefiphopy",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    )
