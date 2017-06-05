import time

from nltk.tag.stanford import StanfordNERTagger

# init Stanford NER with NLTK 
st = StanfordNERTagger('./stanford_ner/classifiers/english.all.3class.distsim.crf.ser.gz','./stanford_ner/stanford-ner.jar')

class TaggedDoc(object):


	def __init__(self, payload, payload_type=False):

		self.payload = payload
		self.payload_type = payload_type
		self.tags = None
		self.locations = []
		self.people = []
		self.organizations = []


	def analyze(self):

		stime = time.time()

		# file path provided
		if self.payload_type == 'file':
			with open(self.file_path, 'r') as f:
				self.tags = st.tag(f.read().split())
		# assume raw text
		else:
			self.tags = st.tag(self.payload.split())

		# parse and save
		for tag in self.tags:

			# locations
			if tag[1] == 'LOCATION':
				self.locations.append(tag[0])

			# people
			if tag[1] == 'PERSON':
				self.people.append(tag[0])

			# organization
			if tag[1] == 'ORGANIZATION':
				self.organizations.append(tag[0])

		# report
		print "took %ss to analyze" % (time.time()-stime)




