import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="community_detection",
    version="0.0.2",
    author="Jiaying Wang",
    author_email="jiaying@sjzu.edu.cn",
    description="A community detection package",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/jiayingwang/community_detection",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=['simple-graph', 'elegant-io'],
    python_requires='>=3.6',
)
