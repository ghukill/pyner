import copy
import json
import os
import sys

# import pyner
from pyner import st, TaggedDoc

'''
Specifically, for DPL letter scans.

Some curatorial decisions:
	- removing multiple instances of the same term from a document
	- grouping terms together so not, "Abraham (PERSON)", "Lincoln (PERSON" but instead "Abraham Lincoln (PERSON)"
	- removed all terms that begin, or include, "Kodak" from digitization target
	- clean up bits of punctuation
'''

def dpl_tag_cleaner(tags):

	# loop through to remove instances of "kodak"
	tags[:] = [tag for tag in tags if 'kodak' not in tag[0].lower()]
	tags[:] = [tag for tag in tags if 'color control patches' not in tag[0].lower()]

	# loop through and remove trailing puncuation
	for tag in tags:
		tag = (tag[0].rstrip("."), tag[1])
		tag = (tag[0].rstrip(","), tag[1])

	# remove dupes and return
	return list(set(tags))


def walk_for_texts(root_dir, output_dir):

	'''
	End goal: FILENAME.csv for tags from each .txt file, ner_tags.json for all files at root_dir
	'''

	# prepare json
	json_report = {}
	
	print "walk root dir: %s" % root_dir

	# walk directories 
	walker = os.walk(root_dir)
	
	# bump root
	walker.next()

	# iterate through directories
	for step in walker:

		# create node in dictionary
		dir_name = step[0].split("/")[-1]

		json_report[dir_name] = []
		
		# note location
		print "working on directory: %s" % step[0]

		# process files
		text_files = [f for f in step[2] if f.endswith('.txt')]
		for text_file in text_files:

			# full path
			text_file_path = os.path.join(step[0], text_file)
			print "analyzing file: %s" % text_file_path

			# instantiate TaggedDoc
			doc = TaggedDoc(text_file_path, is_file=True)

			# analyze
			doc.analyze(tag_filter=dpl_tag_cleaner)

			# write csv file
			doc.write_csv(os.path.join(output_dir,"%s.csv" % text_file.split(".")[0]))

			# append to global JSON
			json_report[dir_name].append({
				text_file.split(".")[0]: doc.tags
				})


	# finally, write json report
	with open(os.path.join(output_dir,'ner_tags.json'),'w') as f:
		f.write(json.dumps(json_report))


if __name__ == '__main__':
	root_dir = sys.argv[1]
	output_dir = sys.argv[2]
	walk_for_texts(root_dir, output_dir)