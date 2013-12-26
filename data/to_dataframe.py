#!/usr/bin/env python

from collections import defaultdict
import pandas as pd
import sys

AUTHORS = ('JAY', 'MADISON', 'HAMILTON')

def create_data_frame(fname):
	"""
	Given a filename fname containing the Project Gutenberg version of the
	Federalist Papers, convert the file's contents to a pandas.DataFrame.
	"""
	with open(fname, 'rU') as f:
		return pd.DataFrame(data=get_papers(f.readlines()))

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
	past_greeting = False		# "To the People..." indicates paper's start

	for line in flines:
		line = line.strip()
		if line.startswith("FEDERALIST"):
			papers[paper_count]['contents'] = (' '.join(current_paper))
			papers[paper_count]['author'] = current_author
			current_paper = []
			current_author = None
			past_greeting = False

			# There are two No. 70s in Project Gutenberg. Assign random
			# number to the duplicate paper.
			paper_count = int(line.split(' ')[-1])
			paper_count = 100 if paper_count in papers else paper_count

		# Consume header for each paper. Preserve author.
		if not past_greeting:
			if any(result != -1
					for result in [line.find(author) for author in AUTHORS]):
				current_author = line
			if line.find("To the People of the State of New York:") != -1:
				past_greeting = True
			continue

		current_paper.append(line)
	return papers

if __name__ == "__main__":
	fname = sys.argv[1]
	create_data_frame(fname)
