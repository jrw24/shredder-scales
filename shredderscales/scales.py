"""
class with common scales:

"""

class Scales(object):
	"""
	The scales class stores mutliple attributes:
		- available_scales -> all scales present for plotting
		- scale_alias -> dict mapping common scale names to alternate names
		- interval_dict -> dict mapping interval distance to shorthand name

	"""

	"""
	available_scales are entered as a dictionary with a list of lists:
		- 'name':[[semitones-from-root], [scale-degrees]]
		- ex: 'minor' : [[0,2,3,5,7,8,10], ['1','2','b3','4','5','b6','b7']]
	"""

	available_scales = {
		'chromatic' : [
			[0,1,2,3,4,5,6,7,8,9,10,11],
			['1','b2','2','b3','3','4','b5','5','b6','6','b7','7']],
		'major' : [
			[0,2,4,5,7,9,11], 
			['1','2','3','4','5','6','7']],
		'minor' : [
			[0,2,3,5,7,8,10], 
			['1','2','b3','4','5','b6','b7']],
		'harmonic-minor' : [
			[0,2,3,5,7,8,11],
			['1','2','b3','4','5','b6','7']],
		'pentatonic-major': [
			[0,2,4,7,9],
			['1','2','3','5','6',]],
		'pentatonic-minor': [
			[0,3,5,7,10],
			['1','b3','4','5','b7']],
		'pentatonic-blues': [
			[0,3,5,6,7,10],
			['1','b3','4','b5','5','b7']],
		'pentatonic-neutral': [
			[0,2,5,7,10],
			['1','2','4','5','b7']],
		'ionian' : [
			[0,2,4,5,7,9,11], 
			['1','2','3','4','5','6','7']],
		'dorian' : [
			[0,2,3,5,7,9,10],
			['1','2','b3','4','5','6','b7']],
		'phyrgian' : [
			[0,1,3,5,7,8,10],
			['1','b2','b3','4','5','b6','b7']],	
		'lydian' : [
			[0,2,4,6,7,9,11],
			['1','2','3','#4','5','6','7']],
		'mixolydian' : [
			[0,2,4,5,7,9,10],
			['1','2','3','4','5','6','b7']],
		'aeolian' : [
			[0,2,3,5,7,8,10], 
			['1','2','b3','4','5','b6','b7']],
		'locrian': [
			[0,1,3,5,6,8,10],
			['1','b2','b3','4','b5','b6','b7']],
		'diminished' : [
			[0,2,3,5,6,8,9,11],
			['1','2','b3','4','b5','b6','6','7']],
		'diminished-half' : [
			[0,1,3,4,6,7,9,10],
			['1','b2','b3','3','b5','5','6','b7']],	
		'diminished-whole-tone': [
			[0,1,3,4,6,8,10],
			['1','b2','b3','3','b5','b6','b7']],
		'lydian-augmented' : [
			[0,2,4,6,8,9,11],
			['1','2','3','#4','#5','6','7']],
		'lydian-minor' : [
			[0,2,4,6,7,8,10],
			['1','2','3','#4','5','b6','b7']],
		'lydian-diminished' : [
			[0,2,3,6,7,9,11],
			['1','2','b3','#4','5','6','7']],
		'phrygian-major': [
			[0,1,4,5,7,8,10],
			['1','b2','3','4','5','b6','b7']],
		}

	### identical scales with differing names
	scale_alias = {
		'minor' : ['natural-minor'],
		'pentatonic-major': ['diatonic'],
		'diminished' : ['diminished-whole'],
		'mixolydian' : ['dominant-seventh', 'dominant-7th'],
		'diminished-half' : ['octatonic-h-w']

	}

	### dictionary for storing shorthand notation for intervals
	interval_dict = {
		0 : 'P1',
		1 : 'm2',
		2 : 'M2',
		3 : 'm3',
		4 : 'M3',
		5 : 'P4',
		6 : 'A4',
		7 : 'P5',
		8 : 'm6',
		9 : 'M6',
		10: 'm7',
		11: 'M7'
	}

	# def __init__(self):

		# self.scale = scale
		# self.key = key 
		# self.key_notes = key_notes

	@staticmethod
	def print_all_scales():
		"""
		print available scales to terminal
		"""
		all_scales = list(Scales.available_scales.keys())

		for s in all_scales:
			print(s)


	@staticmethod
	def get_scale_intervals(scale):
		"""
		search available scales and return entry if scale is a match
			- first look through Scales.available_scales to find a match
			- next look through each entry in scale_alias to check alternate names
			- last raise a ValueError if scale is not present

		Input:
			- string with scale choice, ex: 'major'

		Output:
			- dict with scale-name : [[intervals],[degrees]]
			ex: {'major': [[0, 2, 4, 5, 7, 9, 11], ['1', '2', '3', '4', '5', '6', '7']]}
		"""

		scale = scale.lower() ## enforce lowercase
		out_scale = {}
		if scale in Scales.available_scales:
			out_scale[scale] = Scales.available_scales[scale]
		else:
			for alt_scale in Scales.scale_alias:
				if scale in Scales.scale_alias[alt_scale]:
					scale = alt_scale
					out_scale[scale] = Scales.available_scales[scale]

		if len(out_scale) == 1: ## return only 1 scale
			return out_scale
		else:
			raise ValueError(f'chosen scale {scale} is not included currently')


def get_scale_notes(scale, scale_dict, key, key_notes):
	"""
	for a selected scale, get the notes as a function of intervals

	consider chromatic scale from 0 - 12 (one full octive)
	chromatic_notes is range from (0:12) ## doesnt include 12th fret

	| 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10| 11| 12|
	
	C: major
	| C | - | D | - | E | F | - | G | - | A | - | B | C |

	C: minor
	| C | - | D | Eb| - | F | - | G | Ab| - | Bb| - | C |

	Inputs:
		- scale: name of the scale, ex: 'major'
		- scale_dict: dict with name:[[intervals]:[degrees]]
		- key: key to use for the scale
		- key_notes: dict with notes rearranged with key=0 for the index

	Outputs:
		- final_scale: dict with position:key for the scale
			- E-major: {0: 'E', 2: 'F#', 4: 'G#', 5: 'A', 7: 'B', 9: 'C#', 11: 'D#'}
	"""
	final_scale = {}
	note_positions = scale_dict[scale.lower()][0] ## get intervals

	for position, note in key_notes.items():
		if position in note_positions:
			final_scale[position] = note 

	if final_scale[0] != key:
		raise ValueError(f'key_notes: {key_notes} not arranged with key {key} at 0 index')

	return final_scale

def map_degrees_intervals(scale, one_oct, scale_dict, interval_dict):
	"""
	
	Inputs:
		- scale: name of the scale, ex: 'major'
		- scale_dict: dict with name:[[intervals]:[degrees]]
		- one_oct: all valid notes in the scale for a single octave
		- interval_dict is dict with interval notation relative to root note

	Outputs:
		- degree_map_dict: dict with scale degrees instead of notes
		- int_map_dict: dict with intervals instead of notes
	"""

	### get scale degrees:
	degree = dict(zip(scale_dict[scale][0], scale_dict[scale][1]))

	degree_map_dict = {}
	int_map_dict = {}
	for n in one_oct:
		degree_map_dict[one_oct[n]] = degree[n]
		int_map_dict[one_oct[n]] = interval_dict[n]

	return degree_map_dict, int_map_dict