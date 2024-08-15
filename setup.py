from setuptools import setup, find_packages

setup(
    name="your_project_name",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        # Add any dependencies your package requires
    ],
    entry_points={
        'console_scripts': [
            # Add any scripts you want to be able to run from the command line
        ],
    },
)