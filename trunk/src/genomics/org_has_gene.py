#!/usr/bin/python

import csv
import sys

from optparse import OptionParser


def MakeOpts():
    """Returns an OptionParser object with all the default options."""
    opt_parser = OptionParser()
    opt_parser.add_option("-s", "--species_filename",
                          dest="species_filename",
                          help="input CSV with species names and IDs")
    opt_parser.add_option("-g", "--gene_filename",
                          dest="gene_filename",
                          help="input filename with species having gene")
    return opt_parser


def Main():
	options, _ = MakeOpts().parse_args(sys.argv)
	assert options.species_filename and options.gene_filename
	print 'Reading species list from', options.species_filename
	print 'Reading gene data from', options.gene_filename

	gene_holders = set()
	r = csv.DictReader(open(options.gene_filename))
	map(lambda x: gene_holders.add(x.get('Species').lower()), r)
	#print gene_holders

	r = csv.DictReader(open(options.species_filename))
	for row in r:
		kegg_id = row.get('KEGG ID').lower()
		name = row.get('Organism Name')
		#print name, kegg_id,
		print kegg_id in gene_holders
	 


if __name__ == '__main__':
	Main()
