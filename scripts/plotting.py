
import matplotlib
matplotlib.use('Agg')
from matplotlib import pyplot as plt
from matplotlib import patches
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--')

"""


"""

class fretboard(object):
	"""

	"""
	def __init__(fret_number, string_number):
		self.fret_number = fret_number
		self.string_number = string_number


def plotter(fretboard):
	fig, ax = plt.subplots(figsize= (12, 3))

	frets = fretboard.fret_number
	strings = fretboard.string_number

	xmin = 0
	xmax = frets
	ymin = 0
	ymax = strings+1
	fretboard_adj = 0.5

	
	fret_labels = list(range(0,frets+1))
	fret_label_positions = [x-fretboart_adj for x in fret_labels]

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

	for position, note in final_scale.items():
	    circ = patches.Circle((position-fretboard_adj, 1), radius=0.4, color=my_colors['cyan'])
	    ax.add_artist(circ)
	    ax.text(position-fretboard_adj, 1, note, ha='center', va='center', color='white' )

	plt.savefig('/home/jwangen/projects/shredder/shredder-scales/test/test.pdf', format='pdf')

def main():

	args = 

	fb = fretboard()