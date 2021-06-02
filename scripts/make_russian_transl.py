#!/usr/local/bin/pyenv
# for 3.8.2

import os

#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+

#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+

home = os.path.expanduser("~")
''' 
= os.getenv('USERPROFILE') or os.getenv('HOME')
'''

mscrevbase = home + "/Projects/MSC-Rev/"
msc2020base= mscrevbase + "MSC2020/"

outfile = msc2020base + 'russiandraft'

russianfile = open(mscrevbase + '/xmlprodn/SKOS/russian/russian.txt', 'r')

with open(outfile,'w') as f:
	for line in russianfile.readlines():
		code = line[1:6]
		text = line[8:].strip()
		if code != '':
			f.write('<https://msc2020.org/resources/MSC/2020/MSC2020/%s> skos:prefLabel "%s"@rs .\n' % (code, text))
# 			print('<https://msc2020.org/resources/MSC/2020/MSC2020/%s> skos:prefLabel "%s"@rs .' % (code, text))
	f.close

