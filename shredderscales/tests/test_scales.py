import pytest
import shredderscales.scales as scales
from typing import Dict

@pytest.fixture(scope='module')
def v() -> Dict:
	scale_vars = {
		'e_major':{0: 'E', 2: 'F#', 4: 'G#', 5: 'A', 7: 'B', 9: 'C#', 11: 'D#'}
	}
	# scale_vars['e_major'] = {0: 'E', 2: 'F#', 4: 'G#', 5: 'A', 7: 'B', 9: 'C#', 11: 'D#'}
	return scale_vars

@pytest.fixture
def create_scales_object():
	ScaleObj = scales.Scales()
	return(ScaleObj)

@pytest.fixture
def load_avail_scales(create_scales_object) -> Dict:
	avail_scales = create_scales_object.available_scales
	return avail_scales

@pytest.fixture
def load_major_scale(load_avail_scales) -> Dict:
	major_dict = {}
	major_dict['major'] = load_avail_scales['major']
	return major_dict

@pytest.fixture
def load_pentatonic_major_scale(load_avail_scales) -> Dict:
	scale_dict = {}
	scale_dict['pentatonic-major'] = load_avail_scales['pentatonic-major']
	return scale_dict

@pytest.fixture
def load_scale_alias(create_scales_object) -> Dict:
	scale_alias = create_scales_object.scale_alias
	return scale_alias
	

def test_major_scale(load_major_scale):

	scale_intervals = [0,2,4,5,7,9,11]
	scale_degrees = ['1','2','3','4','5','6','7']
	assert list(load_major_scale.keys()) == ['major']
	assert load_major_scale['major'][0] == scale_intervals
	assert load_major_scale['major'][1] == scale_degrees

def test_scale_alias(load_scale_alias):
	assert type(load_scale_alias) is dict 


def test_get_common_scale_major(create_scales_object, load_major_scale ):

	scale = 'major'
	out_scale = create_scales_object.get_scale_intervals(scale)
	# print('out_scale', out_scale)

	assert type(out_scale) is dict
	assert out_scale == load_major_scale

def test_get_alias_scale_diatonic(create_scales_object, load_pentatonic_major_scale):

	scale = 'diatonic'
	## diatonic maps to pentatonic major and tests alias lookup
	out_scale = create_scales_object.get_scale_intervals(scale)

	assert type(out_scale) is dict
	assert out_scale == load_pentatonic_major_scale

def test_get_bogus_scale(create_scales_object):

	## raise a ValueError if scale is not included
	scale = 'bogus'
	with pytest.raises(ValueError):
		out_scale = create_scales_object.get_scale_intervals(scale)

def test_get_scale_notes_e_major_sharps(load_major_scale, v):

	scale = 'major'
	key = 'E'
	key_notes = {
		0: 'E',
		1: 'F',
		2: 'F#',
		3: 'G',
		4: 'G#',
		5: 'A',
		6: 'A#',
		7: 'B',
		8: 'C',
		9: 'C#',
		10: 'D',
		11: 'D#',
		}

	final_scale = scales.get_scale_notes(
		scale= scale,
		scale_dict = load_major_scale,
		key = key,
		key_notes = key_notes)

	assert final_scale == v['e_major']

def test_get_scale_notes_key_not_zero(load_major_scale):
	"""
	Set the key to not be equal to zero in key_notes dict
		This will raise a value error when final_scale[0] != key
	"""

	scale = 'major'
	key = 'C'
	key_notes = {
		0: 'E',
		1: 'F',
		2: 'F#',
		3: 'G',
		4: 'G#',
		5: 'A',
		6: 'A#',
		7: 'B',
		8: 'C',
		9: 'C#',
		10: 'D',
		11: 'D#',
		}

	with pytest.raises(ValueError):
		final_scale = scales.get_scale_notes(
			scale= scale,
			scale_dict = load_major_scale,
			key = key,
			key_notes = key_notes)


def test_map_degrees_intervals(create_scales_object, load_major_scale, v):

	scale = 'major'
	one_oct = v['e_major']
	int_dict = create_scales_object.interval_dict

	interval_vals = list(int_dict.values())
	degree_vals = load_major_scale[scale][1]

	degree_map_dict, int_map_dict = scales.map_degrees_intervals(
		scale = scale, 
		one_oct = one_oct, 
		scale_dict=load_major_scale, 
		interval_dict=int_dict)

	for d in degree_map_dict:
		assert degree_map_dict[d] in degree_vals

	for i in int_map_dict:
		assert int_map_dict[i] in interval_vals

