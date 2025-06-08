from setuptools import setup, find_packages

setup(
    name="tribe-simulation",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        # List your dependencies here, e.g.:
        # 'numpy>=1.21.0',
    ],
    entry_points={
        "console_scripts": [
            # Define command-line scripts if needed
        ],
    },
)
