import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="ruword_frequency",
    version="0.0.1",
    author="Pavel Naydenov",
    author_email="naydenov.p.v@gmail.com",
    description="Library returns word frequence (ipm) by almost all russian words ",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Somewater/ruword_frequency",
    packages=['ruword_frequency'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Natural Language :: Russian"
    ],
    install_requires=['marisa_trie']
)