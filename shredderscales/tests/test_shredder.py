import pytest
import shredderscales.scales as scales
import shredderscales.notes as notes
import shredderscales.shredder as shredder
from typing import Dict
import sys


### shredder.main(scale='major', key='A',tuning='CGCFAD',outdir='/home/jwangen/projects/testing')

@pytest.fixture(scope='module')
def v() -> Dict:
	test_vars = {
		'A_major_CGCFAD_all': {
			'key': 'A',
			'scale': 'major',
			'tuning': 'CGCFAD',
			'flats' : 'sharps',
			'fretnumber': '24',
			'mode' : 'note',
			'outdir' : '.',
			'django' : '0',
		}
	}
	return test_vars


def test_make_Shredder_object_all_options_included(v):
	"""
	very simple test to check that object is created sucessfully
	"""

	test_example = 'A_major_CGCFAD_all'
	svars = v[test_example]

	s = shredder.Shredder(
		scale = svars['scale'],
		key = svars['key'],
		tuning = svars['tuning'],
		flats = svars['flats'],
		fretnumber = svars['fretnumber'],
		mode = svars['mode'],
		outdir = svars['outdir'],
		django = svars['django'],
		custom_scale = None,
		screenWidth = '1200',
		screenHeight = '350'

		)

	assert s is not None
	assert type(s.scale) == str
	assert type(s.key) == str
	assert type(s.tuning) == str

def test_main_key_scale_tuning_only(monkeypatch):

	## passing empty arguments
	monkeypatch.setattr(sys, 'argv', [''])

	kwargs = {
		'key': 'A',
		'scale': 'major',
		'tuning': 'CGCFAD',
		}

	html_fig, scale_info = shredder.main(**kwargs)
	assert html_fig is None

def test_main_key_scale_sys_argv_entry(monkeypatch):

	## passing empty arguments
	monkeypatch.setattr(
		sys,
		'argv', 
		[
			sys.argv[0],
			'--key', 'A',
			'--scale', 'major',
			'--tuning', 'EADGBE',
		]
	)
	kwargs = {
		}

	html_fig, scale_info = shredder.main(**kwargs)
	assert html_fig is None


def test_main_no_key(monkeypatch):

	## passing empty arguments
	monkeypatch.setattr(sys, 'argv', [''])

	kwargs = {
		'scale': 'major',
		'tuning': 'CGCFAD',
		}
	with pytest.raises(KeyError):
		html_fig, scale_info = shredder.main(**kwargs)

def test_main_no_scale(monkeypatch):

	## passing empty arguments
	monkeypatch.setattr(sys, 'argv', [''])

	kwargs = {
		'key': 'A',
		'tuning': 'CGCFAD',
		}
	with pytest.raises(KeyError):
		html_fig, scale_info = shredder.main(**kwargs)


def test_main_key_scale_only(monkeypatch):

	## passing empty arguments
	monkeypatch.setattr(sys, 'argv', [''])
	
	kwargs = {
		'scale': 'major',
		'key': 'A'
		}

	html_fig, scale_info = shredder.main(**kwargs)
	assert html_fig is None


def test_main_set_django_for_html_output_kwargs(monkeypatch):

	## passing empty arguments
	monkeypatch.setattr(sys, 'argv', [''])
	
	kwargs = {
		'key': 'A',
		'scale': 'major',
		'tuning': 'CGCFAD',
		'django': '1'
		}

	html_fig, scale_info = shredder.main(**kwargs)
	### check that an html is output as str
	assert type(html_fig) is str

def test_main_set_django_for_html_output_sys_argv(monkeypatch):

	## passing empty arguments
	monkeypatch.setattr(
		sys,
		'argv', 
		[
			sys.argv[0],
			'--key', 'A',
			'--scale', 'major',
			'--tuning', 'EADGBE',
			'--django', '1',
		]
	)
	kwargs = {
		}
	html_fig, scale_info = shredder.main(**kwargs)
	### check that an html is output as str
	assert type(html_fig) is str

def test_main_custom_scale_command_line(monkeypatch):

	monkeypatch.setattr(
		sys,
		'argv', 
		[
			sys.argv[0],
			'--key', 'A',
			'--scale', '*custom*',
			'--tuning', 'EADGBE',
			'--scale_name', 'newscale',
			'--scale_intervals', '0,1,4,7,8,10,11'
		]
	)
	kwargs = {
		}

	html_fig, scale_info = shredder.main(**kwargs)
	assert html_fig is None


def test_main_set_django_for_html_output_kwargs_custom_scale(monkeypatch):

	## passing empty arguments
	monkeypatch.setattr(sys, 'argv', [''])
	
	kwargs = {
		'key': 'A',
		'scale': 'major',
		'tuning': 'CGCFAD',
		'django': '1',
		'scale_name': 'newscale',
		'scale_intervals': '0,1,4,7,8,10,11'
		}

	html_fig, scale_info = shredder.main(**kwargs)
	### check that an html is output as str
	assert type(html_fig) is str