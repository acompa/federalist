#!/usr/bin/env python

from collections import defaultdict
import pandas
import sys

AUTHORS = ('JAY', 'MADISON', 'HAMILTON')

def create_data_frame(fname):
	"""
	Given a filename fname containing the Project Gutenberg version of the
	Federalist Papers, convert the file's contents to a pandas.DataFrame.
	"""
	with open(fname, 'rU') as f:
		papers = get_papers(f.readlines())

	# TODO (ac) build data frame


def get_papers(flines):
	"""
	Given a file's readlines() flines, split the contents into individual
	papers. Strategy: start new obj whenever encountering the word "FEDERALIST"
	at the start of a new line.
	"""
	papers = defaultdict(dict)
	current_paper = []
	current_author = None
	paper_count = 0
	for line in flines:
		if line.startswith("FEDERALIST"):
			if len(current_paper) > 0:
				papers[paper_count]['contents'] = (' '.join(current_paper))
				papers[paper_count]['author'] = current_author
				current_paper = []
				current_author = None

			# There are two No. 70s in Project Gutenberg. Assign random
			# number to the duplicate paper.
			paper_count = int(line.split(' ')[-1])
			if paper_count in papers:
				paper_count = 100
		if any(result != -1
				for result in [line.find(author) for author in AUTHORS]):
			current_author = line
		current_paper.append(line)
	return papers

if __name__ == "__main__":
	fname = sys.argv[1]
	create_data_frame(fname)
