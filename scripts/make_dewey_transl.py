#!/usr/local/bin/pyenv
# for 3.8.2

import re
import os

#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+
#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+

home = os.path.expanduser("~")
''' 
= os.getenv('USERPROFILE') or os.getenv('HOME')
'''

mscrevbase = home + "/Projects/MSC-Rev/"
msc2020base= mscrevbase + "MSC2020/"

outfile = msc2020base + 'deweydraft'

deweyfile = open(mscrevbase + 'xmlprodn/SKOS/italian/dmr_11.txt', 'rt')

deweycountfile = msc2020base + 'deweycounts'

ddc_codes_used = []
ddc_codes_counts = {}

linecount = 0
with open(outfile,'wt') as f:
	f.write('### Dewey translations\n')
	for line in deweyfile.readlines():
		linecount = linecount + 1
		code = line.split('\t',2)[0]
		text = line.split('\t',2)[1]
#		print (code + ' | ' + text)
		dcodes = text.split('    ')[1].split('  ')
#		print(dcodes)
		for dc in dcodes:
			dcs = dc.strip()
#			print(dcs)
			f.write('<https://msc2020.org/resources/MSC/2020/MSC2020/{0}> msc:matchDewey <https://msc2020.org/resources/MSC/2020/MSC2020/msc2020-fullDD21-{1}> .\n\n'.format(code, dcs))
			if dcs not in ddc_codes_used:
				ddc_codes_used.append(dcs)
				ddc_codes_counts[dcs]= 1
#				print('New ', dcs)
				f.write('''<https://msc2020.org/resources/MSC/2020/MSC2020/msc2020-fullDD21-{1}> rdf:type owl:NamedIndividual , skos:Concept ; 
            dcterms:issued “2011-06-22”^^xsd:date ;
            dcterms:isPartOf <https://msc2020.org/resources/MSC/2020/MSC2020/> ;
            dcterms:isPartOf  <https://www.oclc.org/content/dam/oclc/dewey/ddc23-summaries.pdf> ;
            rdfs:comment """See also for examples <https://deweysearchde.pansoft.de/webdeweysearch/mainClasses.html>"""@en ;
            mscvocab:scope “A full code from DD21”@en ;
            rdf:value “{1}”^^xsd:string.\n\n'''.format(code, dcs))
				ddc_codes_counts[dcs] = int(ddc_codes_counts[dcs]) +1
			else:
				ddc_codes_counts[dcs] = ddc_codes_counts[dcs] + 1
	f.close
            
print('Number of MSC classes mapped: ', linecount,'\n')
print('Number of Dewey classes referenced: ', len(ddc_codes_used),'\n')

with open(deweycountfile, 'wt') as f: 
	f.write('\n============================\n\n')
	f.write('Dewey entry multiplicities as they come to MSC\n')
	f.write('then sorted by DDC key nad by multiplicity.\n')
	f.write('Number of MSC classes mapped: '+ str(linecount) + '\n')
	f.write('Number of Dewey classes referenced: ' + str(len(ddc_codes_used)) + '\n')
	f.write('\n============================\n\n')
	for key, value in ddc_codes_counts.items(): 
		f.write('%s: %s\n' % (key, value))
	f.write('\n\n============================\n\n')
	f.write('SORTED BY KEY')
	f.write('\n\n============================\n\n')
	for key in sorted(ddc_codes_counts.keys()):
		f.write('%s: %s\n' % (key, value))
	f.write('\n\n============================\n\n')
	f.write('SORTED BY DESCENDING MULTIPLICITY')
	f.write('\n\n============================\n\n')
	listofvalues = sorted(ddc_codes_counts.items(), reverse=True, key=lambda x: x[1])
	for elem in listofvalues :
		f.write(str(elem[0]) + "::" + str(elem[1]) + '\n' )

f.close()  

