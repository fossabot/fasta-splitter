from pathlib import Path
from setuptools import setup
import os


def get_version():
    with open(os.path.join(Path(__file__).parent, "VERSION")) as version_file:
        for line in version_file:
            line = line.strip()
            if "major" in line:
                major = line.rsplit("=", 1)[1]
            if "minor" in line:
                minor = line.rsplit("=", 1)[1]
            if "patch" in line:
                patch = line.rsplit("=", 1)[1]
            if "prerelease" in line:
                prerelease = line.rsplit("=", 1)[1]
    if len(prerelease) > 0:
        version = major + "." + minor + "." + patch + "-" + prerelease
    else:
        version = major + "." + minor + "." + patch
    return version


def get_readme():
    with open(os.path.join(Path(__file__).parent, "README.md")) as readme_file:
        readme = readme_file.read()
    return readme


def get_requirements_list():
    with open(os.path.join(Path(__file__).parent, "REQUIREMENTS")) as requirements_file:
        requirements_list = requirements_file.read().splitlines()
    return requirements_list


setup(name="fasta-splitter",
      version=get_version(),
      description="Command line tool to split one multiple sequences fasta file into individual sequences fasta files.",
      long_description=get_readme(),
      long_description_content_type="text/markdown",
      url="https://github.com/alan-lira/fasta-splitter",
      author="Alan Lira",
      author_email="",
      license="MIT",
      platforms=["Operating System :: POSIX :: Linux"],
      classifiers=["Development Status :: 3 - Alpha",
                   "Intended Audience :: Developers",
                   "Intended Audience :: End Users/Desktop",
                   "Intended Audience :: Science/Research",
                   "License :: OSI Approved :: MIT License",
                   "Natural Language :: English",
                   "Operating System :: MacOS",
                   "Operating System :: Microsoft :: Windows :: Windows 10",
                   "Operating System :: POSIX :: BSD :: FreeBSD",
                   "Operating System :: POSIX :: Linux",
                   "Programming Language :: Python :: 3.8",
                   "Topic :: Scientific/Engineering :: Bio-Informatics"],
      packages=["fastasplitter"],
      include_package_data=True,
      install_requires=get_requirements_list(),
      entry_points={"console_scripts": ["fastasplitter=fastasplitter.split_fasta_sequences_file:main"]})
