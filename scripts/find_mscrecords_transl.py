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
from collections import deque


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

#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+

home = os.path.expanduser("~")
''' 
= os.getenv('USERPROFILE') or os.getenv('HOME')
'''

mscrevbase = home + "/Projects/MSC-Rev/"
msc2020base= mscrevbase + "msc2020/"

basicfile = open(msc2020base + 'msc-2020-suggestion3-imkt.ttl','r')

code_list = open(msc2020base + '/scripts/hash_msccode','r')

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

cnt = 0

msccodes = code_list.read().splitlines()
# print(len(msccodes[1:5]))

dispcodes = [int(code[1:6])-3 for code in msccodes]
dc = deque(dispcodes)
dc.rotate(-1)
dc = list(dc)
dc.pop()
#dc.append(['97-11',dc[-1],len(basicfile.read().splitlines())])
dc.append([msccodes[-1][-5:],int(msccodes[-1][1:6]),69709][2])
# print(dc[-1])
# later derive that last figure rather than hard-code it

whole_file = basicfile.read().splitlines()
# preamble runs until just before the first msc code record
preamble = whole_file[1:int(msccodes[1][1:6]) - 1]
# postamble runs from just after final msc code record to eof
# print(dc[1:5])
# print(dc[-1])
postamble = whole_file[int(dc[-1]) + 1:]
# print(postamble)
# rest is what we read one record at a time and process 
# cd has the msc codes and the record begin line numbers 
# dc already has the record end line numbers
cd = [[code[-5:],code[1:6]] for code in msccodes]
# print(cd[0])

pref_lab = re.compile(r'\s+skos:prefLabel') # "*"@en
record_end = re.compile(r'\s.') 

outfile.write('\n'.join(preamble))
outfile.write('\n')

for c,d in zip(cd,dc):
	record = whole_file[int(c[1]):d]
#		print(c,c[1],d)
#	print(c,c[1],d)
#	record = whole_file[4553:4559]
#	print('\n'.join(record))
	recout = ""
	pref_text = ""
	addl_text = ""
	for rline in record:
		pref_match = pref_lab.match(rline)
		if pref_match == None:
			out_text = rline + '\n'
			outfile.write(out_text)
#			print(None)
#			print(rline)
		else:
			pref_beg = pref_match.end() 
#			print(pref_beg)
			if record_end.match(rline):
				pm = record_end.match(rline)
				pref_end = pm.start()
				print(len(rline), [[[pref_beg, pref_end)
#				pref_text = rline[pref_beg, pref_end]
			else:
				pref_text = rline
			if code in italiankeys:
				addl_text = addl_text + ', \n'+ italiandict[code] + '@it'
#				print(addl_text)
				if code in chinesekeys:
					addl_text = addl_text + ', \n'+ chinesedict[code] + '@zh'
#					print(addl_text)
			out_text = pref_text + addl_text + ' .\n'
			outfile.write(out_text)

outfile.write('\n')
outfile.write('\n'.join(postamble))

