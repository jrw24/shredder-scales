"""
common tunings:

"""

class Tunings(object):

	def __init__(self, scale, key, key_notes):

		self.scale = scale
		self.key = key 
		self.key_notes = key_notes

	def look_up_scale_intervals(self):

		"""
		for a selected scale, get the intrvals present in scale

		
		"""


