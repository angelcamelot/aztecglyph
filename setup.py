from setuptools import setup, find_packages

setup(
    name="aztecglyph",
    version="1.0.2",
    packages=find_packages(exclude=["tests"]),
    author="Angel Camelot",
    author_email="dupeyron.camelot@gmail.com",
    description="Instances of the AztecGlyph class represent 64-bit UUIDs.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/angelcamelot/aztecglyph",
    entry_points={
        "console_scripts": [
            "aztecglyph = aztecglyph.__main__:main",
        ],
    },
    incude_package_data=True,
    install_requires=[],
    extras_require={
        "django": ["django>=3.2"],
        "peewee": ["peewee>=3.14.4"],
    },
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],
)
