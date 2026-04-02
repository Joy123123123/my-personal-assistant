from setuptools import setup, find_packages

setup(
    name="my-personal-assistant",
    version="0.1.0",
    packages=find_packages(exclude=["tests*"]),
    python_requires=">=3.8",
    install_requires=[
        "python-dateutil>=2.8.2",
    ],
    entry_points={
        "console_scripts": [
            "assistant=main:main",
        ],
    },
)
