import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="WebsiteDL-pkg-MateoWatelet",
    version="0.0.1",
    author="Matéo Watelet",
    author_email="mateo.watelet@gmail.com",
    description="download the html files of a website and create a m*n table of the wbsite",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="",
    project_urls={
        "Bug Tracker": "",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: Linux, MacOs",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.6",
)