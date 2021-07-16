from pathlib import Path
from setuptools import setup


def get_version(major: int,
                minor: int,
                patch: int,
                prerelease: str):
    if len(prerelease) > 0:
        version = str(major) + "." + str(minor) + "." + str(patch) + "-" + prerelease
    else:
        version = str(major) + "." + str(minor) + "." + str(patch)
    return version


def get_major(line: str):
    major = 0
    if "major" in line:
        major = int(line.rsplit("=", 1)[1])
    return major


def get_minor(line: str):
    minor = 0
    if "minor" in line:
        minor = int(line.rsplit("=", 1)[1])
    return minor


def get_patch(line: str):
    patch = 0
    if "patch" in line:
        patch = int(line.rsplit("=", 1)[1])
    return patch


def get_pre_release(line: str):
    pre_release = ""
    if "pre_release" in line:
        pre_release = str(line.rsplit("=", 1)[1])
    return pre_release


def parse_version_file():
    with open(Path(__file__).parent.joinpath("VERSION")) as version_file:
        for line in version_file:
            line = line.strip()
            major = get_major(line)
            minor = get_minor(line)
            patch = get_patch(line)
            pre_release = get_pre_release(line)
    return get_version(major, minor, patch, pre_release)


def get_readme():
    with open(Path(__file__).parent.joinpath("README.md")) as readme_file:
        readme = readme_file.read()
    return readme


def get_requirements_list():
    with open(Path(__file__).parent.joinpath("requirements.txt")) as requirements_file:
        requirements_list = requirements_file.read().splitlines()
    return requirements_list


setup(name="fasta-splitter",
      version=parse_version_file(),
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
                   "Programming Language :: Python :: 3.6",
                   "Programming Language :: Python :: 3.7",
                   "Programming Language :: Python :: 3.8",
                   "Programming Language :: Python :: 3.9",
                   "Topic :: Scientific/Engineering :: Bio-Informatics"],
      packages=["fastasplitter"],
      include_package_data=True,
      install_requires=get_requirements_list(),
      entry_points={"console_scripts": ["fastasplitter=fastasplitter.split_fasta_sequences_file:main"]})
