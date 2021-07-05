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

outfile = msc2020base + 'chinesedraft'

chinesefile = open(mscrevbase + '/xmlprodn/SKOS/chinese/MSC2010-Chinese.tsv', 'r')

with open(outfile,'w') as f:
	for line in chinesefile.readlines():
		[code,text] = line.split('\t')
		text = text.strip()
		f.write('<https://msc2020.org/resources/MSC/2020/MSC2020/%s> skos:prefLabel "%s"@zh .\n' % (code, text))
		print('<https://msc2020.org/resources/MSC/2020/MSC2020/%s> skos:prefLabel "%s"@zh .' % (code, text))
	f.close

