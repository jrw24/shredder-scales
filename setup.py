from setuptools import setup, find_packages

setup(
	name='shredderscales',
	version='0.1.4',
	packages=find_packages(
		include=['shredderscales', 'shredderscales.*']),
	install_requires=[
		'matplotlib>=3.10',
		],
	entry_points={
		'console_scripts': [
			'shredder-scales = shredderscales.shredder:main']
	}
)
