from setuptools import setup, find_packages

with open("requirements.txt") as f:
	install_requires = f.read().strip().split("\n")

# get version from __version__ variable in angola_erp_paddle/__init__.py
from angola_erp_paddle import __version__ as version

setup(
	name="angola_erp_paddle",
	version=version,
	description="Using PaddleOCR to scan Vehicle Plates...",
	author="Helkyds",
	author_email="hcesar@gmail.com",
	packages=find_packages(),
	zip_safe=False,
	include_package_data=True,
	install_requires=install_requires
)
