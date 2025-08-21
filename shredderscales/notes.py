"""
Create object with all possible notes and indexes

	start with A == 0

"""


class Notes(object):

	"""
	Notes object contains dictionaries storing fixed values for sharps and flats

	get_notes(sharps_or_flats) returns these dictionaries

	"""

	sharps = {
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

	flats = {
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


	def get_notes(sharps_or_flats):

		note_choice = sharps_or_flats.lower()

		if note_choice == 'sharps':
			notes = Notes.sharps
		elif note_choice == 'flats':
			notes = Notes.flats
		else:
			raise ValueError('Note choice must be either "sharps" or "flats"')

		return notes

def rearrange_notes(key, notes, sharps_or_flats):
	"""
	Rearrange notes so that the key position is equal to 0

	Inputs:
		- key: key for the scale: "E"
		- notes: all_notes with either sharps of flats
		- sharp_or_flats: choice of 'sharps' or 'flats'

	Outputs:
		- new_notes: all notes rearranged so that key index == 0
			- ex: for E major with sharps
			- key_notes: {0: 'E', 1: 'F', 2: 'F#', 3: 'G', 4: 'G#', 5: 'A', 
				6: 'A#', 7: 'B', 8: 'C', 9: 'C#', 10: 'D', 11: 'D#'}
	"""

	## First find position of the key note
	try:
		for position, note in notes.items():
			if note == key:
				key_index = position
		# key_index = notes[self.key]
	except KeyError:
		print(f'key: {key} is not found in selected notes')
		print(f'currently notes are: {sharps_or_flats}')
		print(notes)

	## reorder keys in new dict so that key position == 0
	if key_index != 0:
		new_notes = notes.copy()

		for position, note  in notes.items():
			note_position = position + key_index

			if note_position < len(new_notes):
				new_notes[position] = notes[position+key_index]
			else:
				new_notes[position] = notes[position+key_index-len(new_notes)]

	else:
		new_notes = notes.copy()

	return new_notes

def convert_sharps_to_flats(note_list):
	"""
	change sharps to flats
	"""

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
	"""
	change flats to sharps
	"""

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

