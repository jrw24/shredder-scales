from setuptools import setup, find_packages

with open("README.md", 'r') as f:
	description = f.read()

setup(
	name='shredderscales',
	version='1.0.5',
	author='Jamie Wangen',
	liscense='MIT',
	url = 'https://github.com/jrw24/shredder-scales',
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
	},
	description= 'Guitar-scales for any key and tuning',
	long_description=description,
	long_description_content_type='text/markdown'
)

