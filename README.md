# shredder-scales

shredder-scales is a python package that allows look-up of 
guitar scales given a key, scale, and tuning and outputs
a plot showing the valid note positions on the fretboard. 

The program accepts any number of guitar strings and any tuning 
without restriction to standard tunings. The number of guitar
strings will be set based on the entered tuning.

For example: 
	- 'EADGBE' will set standard 6-string tuning
	- 'G#D#G#C#F#A#D#' will set drop G# 7-string tuning
	- 'F#BEADGBE' will set standard 8-string tuning

## Installation

Use the package manager [pip](https://pypi.org/project/pip/) for installation

```bash
pip install shredderscales
```

## Options
	required:
	--scale: scale to use for retrieiving notes, ex:'major'
	--key: key to use for choosing notes, ex:'C'
	
	optional:
	--tuning: tuning of guitar for plotting notes, ex:'EADGBE'
	--flats: whether to use sharps or flats for accidentals
	--fretnumber: number of frets to plot, max==24 
	--mode: mode to display notes on scale['note', 'degree', 'interval']
		- note will display the note at each position: 'C', 'Eb', ect.
		- degree will display degree in that scale: '1', 'b2', '#4', ect.
		- interval will display the distance from root note: 'M2', 'P5', 'm6'
	--outdir: directory for saving output plot if run locally
	--django: set to '1' for outputing figure as html


## Usage

example command line usage:

```bash
shredder-scales --scale='major' --key='F' --tuning='CGCFAD' --outdir='/path/to/outdir'
```

to print out all available scales:

```bash
shredder-scales-available
```

example python usage"

```python
from shredderscales import shredder

shredder.main(scale='minor', key='G', tuning='BEADGBE')
```

## Contributing

Pull requests and issues are welcome!
