import sys
sys.path.append('/home/jwangen/projects/shredder/shredder-scales/scripts/')
import notes

def main():

	Notes = notes.Notes(sharpsOrFlats = 'sharps')

	print(Notes)

	print(Notes.sharpsOrFlats)

	n = Notes.get_notes()
	print(n)



main()