"""
Shredder-scales: 
	- a python program to retrive notes from scales based on tuning

"""

import sys
import os 
import subprocess
script_path = os.path.abspath(__file__)
script_directory = os.path.dirname(script_path)
sys.path.append('/home/jwangen/projects/shredder/shredder-scales/scripts/')

##
import tunings
import scales
import notes
import argparse
import re 
from matplotlib import pyplot as plt
from matplotlib import patches

parser = argparse.ArgumentParser(
			prog='shredder-scales',
			description='lookup scales based on key and tuning')

parser.add_argument('-s', '--scale' , help='scale of choice for returing notes')
parser.add_argument('-t', '--tuning', 
	help='guitar tuning entered from lowest pitch to highest ex: CGCFAD or EbAbDbGbBbEb',
	default='EADGBE')
parser.add_argument('-k', '--key', help='key for this scale')
parser.add_argument('-f', '--flats', default='auto', help='whether to use flat notation: [sharps, flats, auto]')
parser.add_argument('-n', '--fretnumber', default='24', help='number of frets to use for plotting')
parser.add_argument('-o', '--outdir', default=script_directory, help='directory for saving scripts' )

class Shredder(object):
	def __init__(self, scale, key, tuning, flats, fretnumber, outdir):
		self.scale = scale 
		self.key = key 
		self.tuning = tuning 
		self.flats = flats 
		self.fretnumber = int(fretnumber)
		self.outdir = outdir

	def check_valid_tuning(self):
		if '#' in self.tuning and 'b' in self.tuning:
			print(self.tuning)
			raise Exception('Invalid tuning containg sharps(#) and flats(b)')
			sys.exit()

	def set_key_accidentals(self):
		if '#' in self.key:
			self.flats = 'sharps'
		elif 'b' in self.key:
			self.flats = 'flats'
		elif '#' in self.tuning:
			self.flats = 'sharps'
		elif 'b' in self.tuning:
			self.flats = 'flats'
		else: ## default to sharps
			self.flats = 'sharps'

	def parse_tuning(self):
		"""
		Take the entered tuning and parse into a list
			be wary of checking for sharps and flats
			sharps: #
			flats: b
		Inputs:
			- Tuning entered as a string with # or b
			- Example: 'CGCFAD' or 'G#D#G#C#F#A#D#'

		Outputs:
			- list with note of each sting as 1 entry
			- Example: ['G#', 'D#', 'G#', 'C#', 'F#', 'A#', 'D#']
		"""
		
		## check that tuning only includes valid characters
		tuning_valid_chars = ['A', 'B', 'C', 'D', 'E', 'F', 'G', '#', 'b']
		for c in self.tuning:
			if c in tuning_valid_chars:
				continue
			else:
				raise Exception(f'Invalid character in tuning entry: {c}')

		## split tuning into a list of one note per string
		tuning_list =[]
		tuning_special_chars = ['#', 'b'] # sharps or flats

		for i in range(len(self.tuning)):	    
			current_tune = self.tuning[i]
			if current_tune in tuning_special_chars:
				continue
			elif i == len(self.tuning)-1:
				tune = current_tune
			elif self.tuning[i+1] in tuning_special_chars: # look ahead
				tune = current_tune+self.tuning[i+1]
			else:
				tune = current_tune
			tuning_list.append(tune)
		return tuning_list

	def calculate_tuning_intervals(self, tuning_list, note_dict):
		"""
		Determine number of semitones (half-steps) between notes in tuning

		Inputs:
			- tuning_list is a list with each string as an entry
				ex: ['C', 'G', 'C', 'F', 'A', 'D']
			- note dictionary with index:note and proper sharp/flat entry

		Outputs:
			- list with intervals between each notes in spacing
				- length should be 1 shorter than tuning_list
				- assumes increasing pitch between notes
		"""
		interval_list = []
		octave = 12
		second_octave = {}

		for n in note_dict:
			second_octave[n+octave] = note_dict[n]
		expanded_notes = note_dict | second_octave

		for t in range(len(tuning_list)):
			if t == len(tuning_list)-1: ## skip last note		
				continue
			lower_interval = -1
			upper_interval = -1
			current_note = tuning_list[t]
			next_note = tuning_list[t+1]
			for position, note, in expanded_notes.items():
				if note == current_note:
					lower_interval = position
				if note == next_note:
					if lower_interval != -1:
						upper_interval = position
						intreval_distance = upper_interval - lower_interval
						interval_list.append(intreval_distance)
						break
		return interval_list

	def build_scales_per_string(self, scale_notes_one_octave, tuning_list, interval_list):
		"""
		Take a selected scale, and calculate note positions relative to tuning

		Inputs:
			- scale_notes_one_octave
				- dictionary with postion:note for only selected notes in chosen scale
				- ex: {0: 'D', 2: 'E', 3: 'F', 5: 'G', 7: 'A', 8: 'A#', 10: 'C', 12: 'D'}
			- tuning_list
				- list with tuning at each string in ascending pitch
				- ex: ['C', 'G', 'C', 'F', 'A', 'D']

		Outputs:
			- string_scales_list
				- list with adjusted tunings for full two octaves on each string
				- each entry of list is adjusted scale-dictionary
				- example with D minor for CGCFAD tuning:
				[
				{0: 'C', 2: 'D', 4: 'E', 5: 'F', 7: 'G', 9: 'A', 10: 'A#', 12: 'C', 14: 'D', 16: 'E', 17: 'F', 19: 'G', 21: 'A', 22: 'A#', 24: 'C'}
				{0: 'G', 2: 'A', 3: 'A#', 5: 'C', 7: 'D', 9: 'E', 10: 'F', 12: 'G', 14: 'A', 15: 'A#', 17: 'C', 19: 'D', 21: 'E', 22: 'F', 24: 'G'}
				{0: 'C', 2: 'D', 4: 'E', 5: 'F', 7: 'G', 9: 'A', 10: 'A#', 12: 'C', 14: 'D', 16: 'E', 17: 'F', 19: 'G', 21: 'A', 22: 'A#', 24: 'C'}
				{0: 'F', 2: 'G', 4: 'A', 5: 'A#', 7: 'C', 9: 'D', 11: 'E', 12: 'F', 14: 'G', 16: 'A', 17: 'A#', 19: 'C', 21: 'D', 23: 'E', 24: 'F'}
				{0: 'A', 1: 'A#', 3: 'C', 5: 'D', 7: 'E', 8: 'F', 10: 'G', 12: 'A', 13: 'A#', 15: 'C', 17: 'D', 19: 'E', 20: 'F', 22: 'G', 24: 'A'}
				{0: 'D', 2: 'E', 3: 'F', 5: 'G', 7: 'A', 8: 'A#', 10: 'C', 12: 'D', 14: 'E', 15: 'F', 17: 'G', 19: 'A', 20: 'A#', 22: 'C', 24: 'D'}
				]
		"""
		string_scales_list = []
		max_octaves = 2
		# one_octave = 12
		# two_octave = 24
		note_quantity = len(scale_notes_one_octave)
		print('note_quantity', note_quantity)
		# scale_notes_one_octave[one_octave] = scale_notes_one_octave[0]
		current_scale = add_octave(scale_notes_one_octave.copy())

		for i in range(len(tuning_list)):
			print(f'--starting string {i+1}--')
			## check to see if the key matches first string in tuning
			if i == 0 and tuning_list[i] == current_scale[i]: 
				## no adjustment needed, simply add first string to output list
				string_scales_list.append(current_scale.copy())
			
			else:
				next_scale = {}
				out_of_bounds_keys = []
				current_scale = add_octave(current_scale.copy())
				## adjust tuning for first string
				if i == 0:
					current_note = tuning_list[i]
					interval_offset = min([(k,v) for (k,v) in current_scale.items() if v ==current_note])[0]
				## adjust tuning for subsequent strings
				else:
					interval_offset = interval_list[i-1]

				for i in current_scale:
					next_scale[i - interval_offset] = current_scale[i]
				for j in next_scale:
					if j < 0:
						out_of_bounds_keys.append(j)
					# elif j > note_quantity*max_octaves:
					# 	out_of_bounds_keys.append(j)
					else:
						pass
				for k in out_of_bounds_keys:
					del next_scale[k]
				## trim to two octave of notes:
				next_scale = dict(list(next_scale.items())[:note_quantity*max_octaves])
				string_scales_list.append(next_scale)
				current_scale = next_scale.copy()

		return string_scales_list

	def shred(self):
		"""
		Given a scale, key, and tuning with sharp or flats specified
			split the tuning into a list
			calculate intervals between notes in tuning
			return all notes in a given scale
			starting with the key as the root note [0]

		Inputs:
			- scale of choice, ex: 'major' or 'minor'
			- key for the scale, ex: 'C' or 'D#' or 'Gb'

		Outpus:
			- tuning_list with one note per entry
			- interval_list with spacing between intrevals
			- scale_notes 
		"""
		## first check that tuning is valid
		self.check_valid_tuning()

		## set accidentals to use if not specified
		if self.flats == 'auto':
			self.set_key_accidentals()
			print(f'using {self.flats} as accidentals')

		## create a list with an entry for each string note
		tuning_list = self.parse_tuning()

		## create a Notes object for the given scale
		note = notes.Notes(self.flats, self.key)

		## retrieve all possible notes dict for sharp or flat designation
		all_notes = note.get_notes()

		## get interval distance for selected tuning
		interval_list = self.calculate_tuning_intervals(tuning_list, all_notes)

		## rearrange notes so that the key is the root note: notes[0] = key
		key_notes = note.rearrange_notes(all_notes)

		## create a scale object with notes in proper order
		scale = scales.Scales(self.scale, self.key, key_notes)

		## select only notes to be included in the scale of choice
		scale_notes_one_octave = scale.get_scale_notes()

		## make a list of scale_dicts for each string
		string_scales_list = self.build_scales_per_string(
								scale_notes_one_octave, 
								tuning_list,
								interval_list)

		print('string_scales_list')
		for s in string_scales_list:
			print(s)

		## trim scales to fretboard size
		string_scales_list = self.mod_fretboard(string_scales_list)
		print('string_scales_list, trimmed')
		for s in string_scales_list:
			print(s)

		return (tuning_list, interval_list, string_scales_list)

	def mod_fretboard(self, string_scales_list):
		# octave = 12
		# expanded_scale = {}
		# if max(scale_notes.keys()) < self.fretnumber:
		# 	for position in scale_notes:
		# 		expanded_scale[position+octave] = scale_notes[position]
		# final_scale = scale_notes | expanded_scale

		max_frets = 24
		if self.fretnumber > max_frets:
			raise Exception(f'fret number exceeds max of {max_frets}')

		for gs in string_scales_list: ## gs -> guitar string
			## for 24 fret special case:
			if self.fretnumber == 24:
				if list(gs.keys())[0] == 0: # open string in scale
					gs[self.fretnumber] = gs[0]
			## if less thant 24 frets then trim:
			else:		
				frets_to_trim = []
				for position in gs:
					if position > self.fretnumber:
						frets_to_trim.append(position)
				for fret in frets_to_trim:
					del gs[fret]
		return string_scales_list


	def plotter(self, tuning_list, string_scales_list):

		## from Bang Wong: https://www.nature.com/articles/nmeth.1618
		my_colors = { 
			'black' :'#000000',
			'orange' : '#ffb000',
			'cyan' :'#63cfff',
			'red' :'#eb4300',
			'green' :'#00c48f',
			'pink' :'#eb68c0',
			'yellow' :'#fff71c',
			'blue' :'#006eb9'
		}
		fig, ax = plt.subplots(figsize= (12, 3))

		frets = range(0,int(self.fretnumber))
		strings = range(0,len(tuning_list))

		xmin = 0
		xmax = self.fretnumber
		ymin = 0
		ymax = len(tuning_list)+1
		fretboard_adj = 0.5

		
		fret_labels = list(range(0,self.fretnumber+1))
		fret_label_positions = [x-fretboard_adj for x in fret_labels]

		ax.set_title(f'{self.key} {self.scale} scale')
		ax.set_yticks([])
		ax.set_xticks(fret_label_positions, fret_labels)

		ax.set_xlim(xmin-fretboard_adj*2,xmax)
		# ax.set_ylim(ymin,ymax)
		ax.set_ylim(ymin-fretboard_adj,ymax+fretboard_adj)
		ax.hlines(ymax-fretboard_adj, xmin, xmax, linestyles ='solid', color = 'black')
		ax.hlines(ymin+fretboard_adj, xmin, xmax, linestyles ='solid', color = 'black')

		for fret in frets:
			ax.vlines(fret, ymin+0.5, ymax-0.5, linestyles = 'solid', color = 'black')
		for guitar_string in strings:
			ax.hlines(ymax-guitar_string-1, xmin, xmax, linestyles ='solid', color = 'grey')
		
		counter = 1
		for gs in string_scales_list:
			for position, note in gs.items():
				if note == self.key:
					circ = patches.Circle((position-fretboard_adj, counter), radius=0.4, color=my_colors['orange'])
				else:
					circ = patches.Circle((position-fretboard_adj, counter), radius=0.4, color=my_colors['cyan'], fill=True)
				ax.add_artist(circ)
				ax.text(position-fretboard_adj, counter, note, ha='center', va='center', color='white')
			counter +=1

		figout = f'{self.outdir}/{self.tuning}-{self.key}-{self.scale}-scale.png'
		plt.savefig(figout, format='png')
		# open_image(figout)



def add_octave(current_scale):
	"""
	add an octave to a scale dictionary
	** This must start and and with a full octave range:
		0, 12, 24, 36, ect.

	Inputs:
		- scale dictionary with position:note structure

	Outputs:
		- additional octave added to end of the scale
	"""
	octave = 12
	new_notes = []
	for i in current_scale:
		new_note = (i+octave, current_scale[i])
		new_notes.append(new_note)
	for n in new_notes:
		current_scale[n[0]] = n[1]
	return current_scale
	

def open_image(path):
	## from stack overflow: https://stackoverflow.com/questions/35304492/python-open-multiple-images-in-default-image-viewer
	imageViewerFromCommandLine = {'linux':'xdg-open',
								  'win32':'explorer',
								  'darwin':'open'}[sys.platform]
	subprocess.run([imageViewerFromCommandLine, path])


def main():
	args = parser.parse_args()
	if not os.path.exists(args.outdir):
		os.makedirs(args.outdir)

	shredder = Shredder(
		args.scale,
		args.key,
		args.tuning,
		args.flats,
		args.fretnumber,
		args.outdir)

	tuning_list, interval_list, string_scales_list = shredder.shred()
	shredder.plotter(tuning_list, string_scales_list)

if __name__ == '__main__':
	main()