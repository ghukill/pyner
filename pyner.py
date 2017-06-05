import csv
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
			with open(self.payload, 'r') as f:
				self.tags = st.tag(f.read().split())
		# assume raw text
		else:
			self.tags = st.tag(self.payload.split())

		# parse and save

		'''
		What we need to do here is group terms that come together.  For example:

		 (u'Federal', u'ORGANIZATION'),
		 (u'Reserve', u'ORGANIZATION'),
		 (u'Bank', u'ORGANIZATION'),
		 (u'of', u'ORGANIZATION'),
		 (u'New', u'ORGANIZATION'),
		 (u'York', u'ORGANIZATION'),
		 (u'and', u'O'),
		 (u'led', u'O'),
		 (u'by', u'O'),
		 (u'Timothy', u'PERSON'),
		 (u'R.', u'PERSON'),
		 (u'Geithner,', u'PERSON'),

		 we should save "Federal Reserve Bank of New York" and "Timothy R. Geithner"
		'''

		# group tags
		self.tags = self._group_consecutives(self.tags)

		# parse
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


	def _group_consecutives(self, tags):
		run = []
		result = []
		expect = None
		last_tag = None
		for value,tag in tags:
			if tag in ['PERSON','LOCATION','ORGANIZATION']:
				last_tag = tag
				if (tag == expect) or (expect is None):
					run.append(value)
					expect = tag
				else:
					run = [value]
					result.append((" ".join(run), last_tag))
			else:
				if len(run) > 0:
					result.append((" ".join(run), last_tag))
				expect = None
				run = []
		if len(run) > 0:
			result.append((" ".join(run), last_tag))
		return result


	def write_csv(self, output_file_path):

		with open(output_file_path,'w') as f:
			writer = csv.writer(f, delimiter=',')
			for tag in self.tags:
				writer.writerow(tag)




