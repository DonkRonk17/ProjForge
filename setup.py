from setuptools import setup

setup(
    name="projforge",
    version="1.0.0",
    description="Project Scaffolding & Template Engine - Generate complete project structures from templates",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    author="ATLAS (Team Brain)",
    author_email="",
    url="https://github.com/DonkRonk17/ProjForge",
    py_modules=["projforge"],
    python_requires=">=3.7",
    entry_points={
        "console_scripts": [
            "projforge=projforge:main",
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: Software Development :: Code Generators",
        "Topic :: Utilities",
    ],
    keywords="scaffolding template project generator cli",
)
