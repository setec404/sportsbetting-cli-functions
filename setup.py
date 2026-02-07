from setuptools import setup, find_packages

setup(
    name="sbcli",
    version="0.1.0",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        "click>=8.1.0",
    ],
    entry_points={
        "console_scripts": [
            "sbcli=sbcli.cli:cli",
        ],
    },
    python_requires=">=3.8",
)
