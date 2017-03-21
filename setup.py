from setuptools import setup, find_packages


with open("README.md") as readme_file:
    readme = readme_file.read()


with open("requirements.txt") as requirements_file:
    requirements = [line.strip() for line in requirements_file]


setup(
    name="pymountebank",
    version="1.0.2",
    author="Quid Inc",
    author_email="infrastructure@quid.com",
    packages=find_packages(exclude=["tests*"]),
    include_package_data=True,
    description="Mountebank wrapper for mocking HTTP APIs",
    long_description=readme,
    install_requires=requirements
)
