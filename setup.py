import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="cosmosdb-bulk-updater",
    version="0.5.0",
    author="Renato Ramos",
    author_email="ramos.renato@outlook.com",
    description="A bulk updater for Microsoft CosmosDB",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/renato04/cosmosdb-bulk-updater",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
