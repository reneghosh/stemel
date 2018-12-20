import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="stemel",
    version="0.0.3",
    author="René Ghosh",
    author_email="rene.ghosh@gmail.com",
    description="stemel polyphonic patterns language",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/satelliteray/stemel",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
