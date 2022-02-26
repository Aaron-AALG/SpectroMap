from setuptools import find_packages, setup

with open("README.rst", "r") as readme:
    long_description = readme.read()

setup(
    name = 'spectromap',
    packages = find_packages(include=['spectromap']),
    version = '0.1.0',
    author = 'Aaron Lopez-Garcia',
    author_email='aaron.lopez@uv.es',
    description = 'SpectroMap is a peak detection algorithm that computes the constellation map for a given signal',
    long_description=long_description,
    license = 'GPL-3.0',
    url='https://github.com/Aaron-AALG/spectromap',
    download_url = 'https://github.com/Aaron-AALG/spectromap/releases/tag/spectromap',
    install_requires=['numpy >= 1.19',
                      'scipy >= 1.6.3'],
    classifiers=["Programming Language :: Python :: 3.8",
			     "License :: OSI Approved :: GPL-3.0 License"],
)
