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



#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+

home = os.path.expanduser("~")
''' 
= os.getenv('USERPROFILE') or os.getenv('HOME')
'''

mscrevbase = home + "/Projects/MSC-Rev/"
msc2020base= mscrevbase + "msc2020/"

basicfile = open(msc2020base + 'msc-2020-suggestion3-imkt.ttl','r')

outfileone = open(msc2020base + '/scripts/hash_msccode','w')
outfiletwo = open(msc2020base + '/scripts/hash_seeFor','w')
outfiletre = open(msc2020base + '/scripts/hash_other','w')
outfilefor = open(msc2020base + '/scripts/hash_non','w')

hashes_start = re.compile(r'^###')
hashes_code = re.compile(r'^###  http://imkt.org/resources/MSC/msc2020/[0-9]')
hashes_seeFor = re.compile(r'^###  http://imkt.org/resources/MSC/msc2020/seeFor')

cnt = 0
code_cnt = 0
seeFor_cnt = 0
other_cnt = 0
nonhash_cnt= 0

for bline in basicfile.readlines():
	cnt += 1
	line = bline.strip()
	m = hashes_start.match(line)
	if m:
		n = hashes_code.match(line)
		if n:
			outfileone.write('L{0:5d}: {1}'.format(cnt, line + '\n'))
			code_cnt += 1
		else:
			n = hashes_seeFor.match(line)
			if n:
				outfiletwo.write('L{0:5d}: {1}'.format(cnt, line + '\n'))
				seeFor_cnt += 1
			else:
				outfiletre.write('L{0:5d}: {1}'.format(cnt, line + '\n'))
				other_cnt += 1
	else:
		outfilefor.write(  'L{0:5d}: {1}'.format(cnt, line + '\n'))
		nonhash_cnt += 1
# 	if (cnt % 500 == 0):
# 		print(str(cnt))

print('Number of lines read = ' + str(cnt))       
print('Number of MSC codes  = ' + str(code_cnt))       
print('Number of seeFor     = ' + str(seeFor_cnt))      
print('Number of others     = ' + str(other_cnt))       
print('Number non hash      = ' + str(nonhash_cnt))       
print('Discrepancy          = ' + str(cnt -code_cnt - seeFor_cnt - other_cnt - nonhash_cnt))       
       
