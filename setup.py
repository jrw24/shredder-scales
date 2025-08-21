from setuptools import setup, find_packages

setup(
	name='shredderscales',
	version='0.1.5',
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

## python setup.py sdist bdist_wheel

## pip install ~/projects/shredder/shredderscales/dist/shredderscales-0.1.5-py3-none-any.whl

## shredder-scales --scale='major' --key='F' --tuning='CGCFAD' --outdir='/home/jwangen/projects/testing'

## shredder.main(scale='major', key='A',tuning='CGCFAD',outdir='/home/jwangen/projects/testing')

## development mode:
## python -m pip install -e .