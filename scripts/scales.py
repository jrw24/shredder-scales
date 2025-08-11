"""
class with common scales:

"""

class Scales(object):

	def __init__(self, scale, key, key_notes):

		self.scale = scale
		self.key = key 
		self.key_notes = key_notes

	def get_scale_notes(self):
		"""
		for a selected scale, get the notes as a function of intervals

		consider chromatic scale from 0 - 12 (one full octive)
		chromatic_notes is range from (0:12) ## doesnt include 12th fret

		| 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10| 11| 12|
		
		C: major
		| C | - | D | - | E | F | - | G | - | A | - | B | C |

		C: minor
		| C | - | D | Eb| - | F | - | G | - | A | Bb| - | C |

		"""

		chromatic_notes = range(0,12)
		octave = 12
		scale_intervals = {
			'chromatic' : [0,1,2,3,4,5,6,7,8,9,10,11],
			'major' : [0,2,4,5,7,9,11],
			'minor' : [0,2,3,5,7,8,10],
			'harmonic-minor' : [0,2,3,5,7,8,11],
			'pentatonic-major': [0,2,4,7,9],
			'pentatonic-minor': [0,3,5,7,10],

			'phrygian-major': [0,1,4,5,7,8,10]


		}

		if self.scale.lower() in scale_intervals:
			final_scale = {}
			note_positions = scale_intervals[self.scale.lower()]

			for position, note in self.key_notes.items():
			    if position in note_positions:
			        final_scale[position] = note
		else:
			raise Exception(f'chosen scale {self.scale} is not included currently')

		return final_scale

