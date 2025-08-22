"""
Shredder-scales: 
	A python program to retrive and plot notes from scales based on tuning

	Arguments:
		Required:
			--scale: scale to use for retrieiving notes, ex:'major'
			--key: key to use for choosing notes, ex:'C'

		Optional:
			--tuning: tuning of guitar for plotting notes, ex:'CGCFAD'
				- defaults to standard 6-string tuning: 'EADGBE'
				- handles any number of strings, and is used to determine strings
					- ex: 'F#BEADGBE' will be standard 8-string tuning
			--flats: whether to use sharps or flats for determinig notes
				- defaults to auto: will determine based on key, then tuning
			--fretnumber: number of frets to plot, max==24 
				- defaults to 24
				- while 30 fret guitars do exist (thanks Ibanez), these are too rare to include for now
			--mode: mode to display notes on scale['note', 'degree', 'interval']
				- note will display the note at each position: 'C', 'Eb', ect.
				- degree will display degree in that scale: '1', 'b2', '#4', ect.
				- interval will display the distance from root note: 'M2', 'P5', 'm6'
			--outdir: directory for saving output plot if run locally
			--django: when run on django based web app, 
				- use mpld3 to display plot instead of saving 
				- see repo here for django app: https://github.com/jrw24/djshred
	Outputs:
		- generates a png plot of the guitar scale

"""

import sys
import os 
current_directory = os.getcwd()

import shredderscales.scales as scales
import shredderscales.notes as notes
import argparse
import matplotlib
matplotlib.use('agg')
from matplotlib import pyplot as plt
from matplotlib import patches
import mpld3

def parse_arguments(args=None):
	parser = argparse.ArgumentParser(
			prog='shredder-scales',
			description='lookup scales based on key and tuning')

	parser.add_argument('-s', '--scale', #required=False, 
 		default=False,
		help='scale of choice for returing notes')
	parser.add_argument('-t', '--tuning', required=False,
		help='guitar tuning entered from lowest pitch to highest ex: CGCFAD or EbAbDbGbBbEb',
		default='EADGBE')
	parser.add_argument('-k', '--key', #required=False,
		default=False,
		help='key for this scale')
	parser.add_argument('-f', '--flats', default='auto', help='whether to use flat notation: [sharps, flats, auto]')
	parser.add_argument('-n', '--fretnumber', default='24', help='number of frets to use for plotting')
	parser.add_argument('-m', '--mode', default='note', help='mode to use for displaying notes: [note, degree, interval]')
	parser.add_argument('-o', '--outdir', default=current_directory, help='directory for saving scripts' )
	parser.add_argument('-d', '--django', default='0', help='perform plotting on django server [0,1]')
	args, _ = parser.parse_known_args() ## return only known args
	return args


class Shredder(object):
	"""
	Core object that contains functions for finding scales

	functions internal to object:
		- check_valid_tuning(self): enforce only sharps or only flats in tuning
		- set_key_accidentals(self): when --flats==auto, set to sharps or flats
		- correct_key_tuning_conflict(self, tuning_list):
			enforce self.flats and tuning_list to use same accidentals as self.key
		- parse_tuning(self): split tuning entry into list with one note per string
		- calculate_tuning_intervals(self, tuning_list, note_dict):
			calculate intervals between notes in tuning
		- build_scales_per_string(self, 
			scale_notes_one_octave, 
			tuning_list, 
			interval_list,
			all_notes): 
			For a selected scale, calculate note positions on each string 
		- mod_fretboard(self, string_scales_list):
			trim the length of the fretboard if self.fretnumber < 24
		
	functions called by main():
		- shred(self):
			core function that performs all calculations
		- plotter(self, tuning_list, string_scales_list, scale_dict, degree_map_dict, int_map_dict)
			plotting function for generating image of scale on fretboard

	"""

	def __init__(self, scale, key, tuning, flats, fretnumber, mode, outdir, django):
		self.scale = scale 
		self.key = key 
		self.tuning = tuning 
		self.flats = flats 
		self.fretnumber = int(fretnumber)
		self.mode = mode
		self.outdir = outdir
		self.django = django

	def check_valid_tuning(self):
		if '#' in self.tuning and 'b' in self.tuning:
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

	def correct_key_tuning_conflict(self, tuning_list):
		"""
		If key clashes with self.flats:
			ex: key='Bb', self.flats='sharps'

			Then:
				reset the flats or sharps to match key
				replace flats or sharps in tuning_list to match key

		Output:
			- self.flats matching the key accidental
			- tuning_list with all notes matching the key accidental
		"""

		if '#' in self.key:
			key_acc = 'sharps'
		elif 'b' in self.key:
			key_acc = 'flats'
		else:
			key_acc = self.flats 

		if key_acc != self.flats:
			## clash here
			self.flats = key_acc

		if self.flats == 'sharps':
			tuning_list = notes.convert_flats_to_sharps(tuning_list)
		if self.flats == 'flats':
			tuning_list = notes.convert_sharps_to_flats(tuning_list)
		return tuning_list

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

	def build_scales_per_string(self, 
			scale_notes_one_octave, 
			tuning_list, 
			interval_list,
			all_notes):
		"""
		Take a selected scale, and calculate note positions relative to tuning

		Inputs:
			- scale_notes_one_octave
				- dictionary with postion:note for only selected notes in chosen scale
				- ex: {0: 'D', 2: 'E', 3: 'F', 5: 'G', 7: 'A', 8: 'A#', 10: 'C', 12: 'D'}
			- tuning_list
				- list with tuning at each string in ascending pitch
				- ex: ['C', 'G', 'C', 'F', 'A', 'D']
			- interval_list
				- list with semitones between each string
				- ex for CGCFAD: [7, 5, 5, 4, 5]

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
		note_quantity = len(scale_notes_one_octave)
		current_scale = add_octave(scale_notes_one_octave.copy())
		all_notes_two_oct = add_octave(all_notes.copy())

		for i in range(len(tuning_list)):
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
					## open string is present in the scale
					if current_note in list(current_scale.values()):
						interval_offset = min([(k,v) for (k,v) in current_scale.items() if v ==current_note])[0]
					## open string is absent in the scale, look up fret with valid note
					else:
						first_note_index = min([(k,v) for (k,v) in all_notes_two_oct.items() if v ==current_note])[0]
						current_note_index = first_note_index
						counter= 0
						while current_note not in list(current_scale.values()):
							counter +=1
							current_note_index+=counter
							current_note = all_notes_two_oct[current_note_index]
						interval_offset = min([(k,v) for (k,v) in current_scale.items() if v ==current_note])[0] - counter

				## adjust tuning for subsequent strings
				else:
					interval_offset = interval_list[i-1]

				for i in current_scale:
					next_scale[i - interval_offset] = current_scale[i]
				for j in next_scale:
					if j < 0:
						out_of_bounds_keys.append(j)
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
		# self.check_valid_tuning()

		## set accidentals to use if not specified
		if self.flats == 'auto':
			self.set_key_accidentals()

		## create a list with an entry for each string note
		tuning_list = self.parse_tuning()
		
		## correct conflicts with key accidentals and self.key
		tuning_list = self.correct_key_tuning_conflict(tuning_list)

		## retrieve all possible notes dict for sharp or flat designation
		all_notes = notes.Notes.get_notes(self.flats)

		## get interval distance for selected tuning
		interval_list = self.calculate_tuning_intervals(tuning_list, all_notes)

		## rearrange notes so that the key is the root note: notes[0] = key
		key_notes = notes.rearrange_notes(self.key, all_notes, self.flats) ## still has all notes

		## look up scale in available scales and get the dict for that scale
		scale_dict = scales.Scales.get_scale_intervals(self.scale)

		## create a scale object with notes in proper order
		scale_notes_one_octave = scales.get_scale_notes(self.scale, scale_dict, self.key, key_notes)

		degree_map_dict, int_map_dict = scales.map_degrees_intervals(
			self.scale, scale_notes_one_octave, scale_dict, scales.Scales.interval_dict)

		## make a list of scale_dicts for each string
		string_scales_list = self.build_scales_per_string(
								scale_notes_one_octave, 
								tuning_list,
								interval_list,
								all_notes)

		## trim scales to fretboard size
		string_scales_list = self.mod_fretboard(string_scales_list)

		return (tuning_list, interval_list, string_scales_list, scale_dict, degree_map_dict, int_map_dict)

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


	def plotter(self, tuning_list, string_scales_list, scale_dict, degree_map_dict, int_map_dict):

		## from Bang Wong: https://www.nature.com/articles/nmeth.1618
		my_colors = { 
			'black' :'#000000',
			'orange' : '#ffb000',
			'cyan' :'#63cfff',
			'red' :'#eb4300',
			'green' :'#00c48f',
			'pink' :'#eb68c0',
			'yellow' :'#fff71c',
			'blue' :'#006eb9',
			'fretboardcolor' : '#6e493982',
		}

		fig, ax = plt.subplots(figsize= (12, 3))

		frets = range(0,int(self.fretnumber))
		strings = range(0,len(tuning_list))

		xmin = -1 #0
		xmax = self.fretnumber
		ymin = 0
		ymax = len(tuning_list)+1
		fretboard_adj = 0.5
		
		fret_labels = list(range(0,self.fretnumber+1))
		fret_label_positions = [x-fretboard_adj for x in fret_labels]

		ax.set_title(f'Key: {self.key},    Scale: {self.scale},    Mode: {self.mode}')
		ax.set_yticks([])
		ax.set_xticks(fret_label_positions, fret_labels)

		ax.set_xlim(xmin-fretboard_adj*2,xmax)
		# ax.set_ylim(ymin,ymax)
		ax.set_ylim(ymin-fretboard_adj,ymax+fretboard_adj)

		## draw fretboard background:
		fretboard_bg = patches.Rectangle(
			(0, ymin+fretboard_adj ),
			self.fretnumber,
			len(tuning_list),
			color=my_colors['fretboardcolor'],
			zorder=0)
		ax.add_patch(fretboard_bg)

		## add fret dots:
		fret_dots = [3,5,7,9,12,15,17,19,21,24]
		for dot in fret_dots:
			if dot <= self.fretnumber:
				if dot % 12 == 0:
					# ax.scatter(dot, )
					ax.scatter(dot-fretboard_adj, fretboard_adj*3, color='white', s=16, zorder=1)
					ax.scatter(dot-fretboard_adj, ymax-fretboard_adj*3, color='white', s=16, zorder=1)
					pass
				else:
					ax.scatter(dot-fretboard_adj, ymax/2, color='white', s=16, zorder=1)


		ax.hlines(ymax-fretboard_adj, 0, xmax, linestyles ='solid', color = 'black')
		ax.hlines(ymin+fretboard_adj, 0, xmax, linestyles ='solid', color = 'black')

		for fret in frets:
			ax.vlines(fret, ymin+0.5, ymax-0.5, linestyles = 'solid', color = 'black')
		for guitar_string in strings:
			ax.hlines(ymax-guitar_string-1, xmin, xmax, linestyles ='solid', color = 'grey')
		note_counter = 1
		for open_note in tuning_list:
			ax.text(xmin-0.5, note_counter, open_note, ha='center', va='center', color='black', fontsize=14)
			note_counter+=1
		
		current_z = max([_.zorder for _ in ax.get_children()])

		counter = 1
		for gs in string_scales_list:
			for position, note in gs.items():
				if note == self.key:
					circ = patches.Circle(
						(position-fretboard_adj, counter), 
						radius=0.4, 
						color=my_colors['orange'], 
						alpha=0.9, 
						zorder=current_z+1)
				else:
					circ = patches.Circle(
						(position-fretboard_adj, counter), 
						radius=0.4, 
						color=my_colors['cyan'], 
						fill=True,
						alpha=0.9,
						zorder=current_z+1)
				ax.add_artist(circ)
				if self.mode == 'note':
					ax.text(
						position-fretboard_adj, 
						counter, 
						note, 
						ha='center', 
						va='center', 
						color='white',
						zorder=current_z+2)
				if self.mode == 'degree':
					ax.text(
						position-fretboard_adj, 
						counter, 
						degree_map_dict[note], 
						ha='center', 
						va='center', 
						color='white',
						zorder=current_z+2)
				if self.mode == 'interval':
					ax.text(
						position-fretboard_adj, 
						counter, 
						int_map_dict[note], 
						ha='center', 
						va='center', 
						color='white',
						zorder=current_z+2)

			counter +=1

		if self.django == '1':
			html_fig = mpld3.fig_to_html(fig)
			return html_fig
		else: 
			figout = f'{self.outdir}/{self.tuning}-{self.key}-{self.scale}-{self.mode}-scale.png'
			plt.savefig(figout, format='png', bbox_inches='tight')
			return None

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
	

def main(**kwargs):
	"""
	main function for running shredderscales

	Inputs:
		command line arguments or dictionary of keyword args

		first dictionary of kwargs is passed
		then command line arguments are parsed using parse_arguments()
			this is a way of adding defaults while also allowing argparse

	Outputs:
		html_fig
			saved to file with django=0
			output to html with django=1
	"""

	args=parse_arguments()
	### convert to dict
	args_main = vars(args)
	for a in args_main:
		if a not in kwargs:
			if args_main[a] is not None:
				kwargs[a] = args_main[a]

	## reworking for unit tests:
	## check required arguments
	if kwargs['scale'] == False:
		raise KeyError(f'scale not selected!')
	if kwargs['key'] == False:
		raise KeyError(f'key not selected!')

	## add default values otherwise
	if 'outdir' not in kwargs:
		kwargs['outdir'] = current_directory
	if 'tuning' not in kwargs:
		kwargs['tuning'] = 'EADGBE'
	if 'flats' not in kwargs:
		kwargs['flats'] = 'auto'
	if 'fretnumber' not in kwargs:
		kwargs['fretnumber'] = '24'
	if 'mode' not in kwargs:
		kwargs['mode'] = 'note'
	if 'django' not in kwargs:
		kwargs['django'] = '0'

	if not os.path.exists(kwargs['outdir']):
		os.makedirs(kwargs['outdir'])

	shredder = Shredder(
		scale = kwargs['scale'],
		key = kwargs['key'],
		tuning = kwargs['tuning'],
		flats = kwargs['flats'],
		fretnumber = kwargs['fretnumber'],
		mode = kwargs['mode'],
		outdir = kwargs['outdir'],
		django = kwargs['django']
		)

	tuning_list, interval_list, string_scales_list, scale_dict, degree_map_dict, int_map_dict = shredder.shred()
	html_fig = shredder.plotter(tuning_list, string_scales_list, scale_dict, degree_map_dict, int_map_dict)
	return html_fig
