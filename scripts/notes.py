"""
Create object with all possible notes and indexes

	start with A == 0

"""


class Notes(object):

	"""

	"""

	def __init__(self, sharps_or_flats, key):
		self.sharps_or_flats = sharps_or_flats
		self.key = key

	def sharps(self):
		notes = {
			0: 'A',
			1: 'A#',
			2: 'B',
			3: 'C',
			4: 'C#',
			5: 'D',
			6: 'D#',
			7: 'E',
			8: 'F',
			9: 'F#',
			10: 'G',
			11: 'G#',
			}
		return notes
	
	def flats(self):
		notes = {
			0: 'A',
			1: 'Bb',
			2: 'B',
			3: 'C',
			4: 'Db',
			5: 'D',
			6: 'Eb',
			7: 'E',
			8: 'F',
			9: 'Gb',
			10: 'G',
			11: 'Ab',
			}
		return notes

	def get_notes(self):

		note_choice = self.sharps_or_flats.lower()
		print(f'using notes: {note_choice}')

		if note_choice == 'sharps':
			notes = self.sharps()
		elif note_choice == 'flats':
			notes = self.flats()
		else:
			raise ValueError('Note choice must be either "sharps" or "flats"')

		return notes

	def rearrange_notes(self, notes):

		## position 
		try:
			for position, note in notes.items():
				print(position, note)
				if note == self.key:
					key_index = position
			# key_index = notes[self.key]
		except KeyError:
			print('key is not found in selected notes')
			print(f'currently notes are: {self.sharps_or_flats}')
			print(notes)

		if key_index != 0:
			new_notes = notes.copy()

			for position, note  in notes.items():
				note_position = position + key_index

				if note_position < len(new_notes):
					new_notes[position] = notes[position+key_index]
				else:
					new_notes[position] = notes[position+key_index-len(new_notes)]

		return new_notes

def convert_sharps_to_flats(note_list):

	sharps_to_flats = {
		'A#' : 'Bb',
		'C#' : 'Db',
		'D#' : 'Eb',
		'F#' : 'Gb',
		'G#' : 'Ab'
	}

	for i in range(len(note_list)):
	    note = note_list[i]
	    if note in sharps_to_flats:
	        note_list[i] = sharps_to_flats[note]

	return note_list

def convert_flats_to_sharps(note_list):

	flats_to_sharps = {
		'Bb' : 'A#',
		'Db' : 'C#',
		'Eb' : 'D#',
		'Gb' : 'F#',
		'Ab' : 'G#'
	}

	for i in range(len(note_list)):
	    note = note_list[i]
	    if note in flats_to_sharps:
	        note_list[i] = flats_to_sharps[note]

	return note_list

