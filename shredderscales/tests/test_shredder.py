import pytest
import shredderscales.scales as scales
import shredderscales.notes as notes
import shredderscales.shredder as shredder
from typing import Dict


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
			'django' : '0'
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
		django = svars['django']

		)

	assert s is not None
	assert type(s.scale) == str
	assert type(s.key) == str
	assert type(s.tuning) == str

def test_main_key_scale_tuning_only():

	kwargs = {
		'key': 'A',
		'scale': 'major',
		'tuning': 'CGCFAD',
		}

	html_fig = shredder.main(**kwargs)
	assert html_fig is None

def test_main_no_key():

	kwargs = {
		'scale': 'major',
		'tuning': 'CGCFAD',
		}
	with pytest.raises(KeyError):
		html_fig = shredder.main(**kwargs)

def test_main_no_scale():

	kwargs = {
		'key': 'A',
		'tuning': 'CGCFAD',
		}
	with pytest.raises(KeyError):
		html_fig = shredder.main(**kwargs)


def test_main_key_scale_only():
	kwargs = {
		'scale': 'major',
		'key': 'A'
		}

	html_fig = shredder.main(**kwargs)
	assert html_fig is None


	

