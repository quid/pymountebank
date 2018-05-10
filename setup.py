from setuptools import setup, find_packages


with open("README.rst") as readme_file:
    readme = readme_file.read()


with open("requirements.txt") as requirements_file:
    requirements = [line.strip() for line in requirements_file]


setup(
    name="pymountebank",
    description="Mountebank wrapper for mocking HTTP APIs",
    license="BSD 3-Clause License",
    version="1.4.0",
    author="Quid Inc",
    author_email="infrastructure@quid.com",
    url="https://github.com/quid/pymountebank",
    packages=find_packages(exclude=["tests*"]),
    include_package_data=True,
    long_description=readme,
    install_requires=requirements,
    classifiers=[
        "Intended Audience :: Developers",
        "License :: OSI Approved :: BSD License",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.6",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ]
)
