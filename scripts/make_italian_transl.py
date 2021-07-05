#!/usr/local/bin/pyenv
# for 3.8.2

import re
import os

#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+

def italianaccents(s):
	'''This replaces Italian accents coded in TeX 
	with their Unicode equivalents.
	'''
	s = s.replace("\'a", "\u00E1")
	s = s.replace("\'e", "\u00E9")
	s = s.replace("\'i", "\u00ED")
	s = s.replace("\'o", "\u00F3")
	s = s.replace("\'u", "\u00FA")
	s = s.replace("\`a", "\u00E0")
	s = s.replace("\`e", "\u00E8")
	s = s.replace("\`E", "\u00C8")
	s = s.replace("\`i", "\u00EC")
	s = s.replace("\`o", "\u00F2")
	s = s.replace("\`u", "\u00F9")
	return s

# print(italianaccents("indicazioni pi\`u specifiche"))
#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+

home = os.path.expanduser("~")
''' 
= os.getenv('USERPROFILE') or os.getenv('HOME')
'''

mscrevbase = home + "/Projects/MSC-Rev/"
msc2020base= mscrevbase + "MSC2020/"

outfile = msc2020base + 'italiandraft'

italianfile= open(mscrevbase + '/xmlprodn/SKOS/italian/msc2000-italian2.tsv', 'rt')

'''
<https://msc2020.org/resources/MSC/2020/MSC2020/20E10> skos:prefLabel "Quasivarieties und Sorten von Gruppen"@de .
'''

with open(outfile,'wt') as f:
	f.write('### Italian translations\n')
	for line in italianfile.readlines():
		code = line.split('\t',2)[0]
		text = italianaccents(line.split('\t',2)[1]).strip()
		f.write('<https://msc2020.org/resources/MSC/2020/MSC2020/{0}> skos:prefLabel "{1}"@it .\n'.format(code, text))
#		f.write('<https://msc2020.org/resources/MSC/2020/MSC2020/%s> skos:prefLabel "%s"@it .' % (code, text))
#		print('<https://msc2020.org/resources/MSC/2020/MSC2020/%s> skos:prefLabel "%s"@it .' % (code, text))
	f.close
		
		
		