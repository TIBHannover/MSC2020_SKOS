#!/usr/local/bin/pyenv
# for 3.8.2

import re
# import string
# import time
# import sys
# import getopt
import os
# import shutil
# import datetime


#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+

def italianaccents(s):
	'''This replaces Italian accents coded in TeX 
	with their Unicode equivalents.
	'''
	s.replace("\'a", "\u00E1")
	s.replace("\'e", "\u00E9")
	s.replace("\'i", "\u00ED")
	s.replace("\'o", "\u00F3")
	s.replace("\'u", "\u00FA")
	s.replace("\`a", "\u00E0")
	s.replace("\`e", "\u00E8")
	s.replace("\`E", "\u00C8")
	s.replace("\`i", "\u00EC")
	s.replace("\`o", "\u00F2")
	s.replace("\`u", "\u00F9")
	return s

#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+

home = os.path.expanduser("~")
''' 
= os.getenv('USERPROFILE') or os.getenv('HOME')
'''

mscrevbase = home + "/Projects/MSC-Rev/"
msc2020base= mscrevbase + "msc2020/"

basicfile = open(msc2020base + 'msc-2020-suggestion3-imkt.ttl','r')
outfile = open(msc2020base + 'skosdraft','w')

italianfile= open(mscrevbase + '/xmlprodn/SKOS/italian/msc2000-italian2.tsv', 'r')
italiandict ={}
for line in italianfile.readlines():
	code = line.split('\t',2)[0]
	text = italianaccents(line.split('\t',2)[1])
	italiandict[code]= text.strip()
#print(italiandict['03A05'])
# had to fix 81R10 in original file; there was an extra line before
# the last two cross-references
italiankeys = italiandict.keys()



chinesefile = open(mscrevbase + '/xmlprodn/SKOS/chinese/MSC2010-Chinese.tsv', 'r')
chinesedict ={}
for line in chinesefile.readlines():
	[code,text] = line.split('\t')
	chinesedict[code]= text.strip() 
#print(chinesedict['03A05'])
chinesekeys = chinesedict.keys()

#print(len(basicfile.readlines()))

filepath = msc2020base + 'msc-2020-suggestion3-imkt.ttl'
#print(filepath)

p = re.compile(r'\/\d{2,2}[-A-Z][\dXx]{2,2}')
q = re.compile(r'\d{2,2}[-A-Z][\dXx]{2,2}')

preflab = re.compile(r'skos:prefLabel "*"@en')


with open(filepath) as fp:
	line = fp.readline().strip()
	cnt = 1
	while (cnt <5000):
#       print("Line {}: {}".format(cnt, line.strip()))
		line = fp.readline().strip()
		addltext = ''
		lcode = line[-6:]
		print(lcode)
		if p.match(lcode):
			print(lcode,line)
			if '### 'in line:
				code = line[-5:]
				print(code,line)
				outfile.write(line)
#			if q.match(code):
#				print("we have a code")
#			else:
#				break
#  	WRONG IN SOME WAY
				while ' .' not in fp.readline().strip()[-3:]:
					line = fp.readline().strip()
					m = preflab.match(line)
					if m == None:
						preftext = ''
					else:
						preftext = m.group() 
					print(preftext)
					if code in italiankeys:
						addltext = addltext + ', '+ italiandict[code] + '@it'
						print(addltext)
					if code in chinesekeys:
						addltext = addltext + ', '+ chinesedict[code] + '@zh'
					outfile.write(preftext + addltext + ' .\n')
					print(preftext + addltext + ' .\n')
#				outfile.write(line)
		cnt += 1
		print(cnt)
	cnt += 1
#	print(cnt)

print(cnt)       
       
'''
filepath = 'Iliad.txt'
with open(filepath) as fp:
   line = fp.readline()
   cnt = 1
   while line:
       print("Line {}: {}".format(cnt, line.strip()))
       line = fp.readline()
       cnt += 1
       
       with open(filepath) as fp:
	line = fp.readline()
	write(outfile, line)
	cnt = 1
	while (cnt <= 10):
       print("Line {}: {}".format(cnt, line.strip()))
       line = fp.readline()
       cnt += 1
       

for line in basicfile.readlines():
	print(line) 
	write(outfile, line)
	if '### ' in line:
		code = line[-1.-5]
		print(code)
'''

