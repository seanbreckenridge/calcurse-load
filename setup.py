import io
from setuptools import setup, find_packages


# Use the README.md content for the long description:
with io.open("README.md", encoding="utf-8") as fo:
    long_description = fo.read()

setup(
    name="calcurse_load",
    version="0.1.0",
    url="https://github.com/seanbreckenridge/calcurse_load",
    author="Sean Breckenridge",
    author_email="seanbrecke@gmail.com",
    description="""Sources events for calcurse from Google Calendar and todo.txt""",
    long_description=long_description,
    long_description_content_type="text/markdown",
    license="MIT",
    packages=find_packages(),
    test_suite="tests",
    install_requires=["gcsa>=0.4.0", "lxml", "cssselect", "tzlocal"],
    python_requires=">=3.7",
    keywords="calendar todo",
    entry_points={
        "console_scripts": [
            "calcurse_load = calcurse_load.__main__:cli",
            "gcal_index = gcal_index.__main__:main",
        ]
    },
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
    ],
)
