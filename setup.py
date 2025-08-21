from setuptools import setup, find_packages

setup(
	name='shredderscales',
	version='1.0.0',
	author='Jamie Wangen',
	packages=find_packages(
		include=['shredderscales', 'shredderscales.*']),
	install_requires=[
		'matplotlib>=3.10',
		'mpld3'
		],
	entry_points={
		'console_scripts': [
			'shredder-scales = shredderscales.shredder:main',
			'shredder-scales-available = shredderscales.scales:Scales.print_all_scales'
			]
	}
)

