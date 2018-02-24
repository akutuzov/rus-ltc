#! /usr/bin/python3
# coding: utf-8

# calculate LEARNER (and learner only!) parallel corpus size, based on FILESOURCES, instead of props
import sys
from xml.dom import minidom
import csv

#use prof_tmx_stats.py for tmx with professional translation. It has no attribute filesource!
arg1 = sys.argv[1] # this is a clean and tidy rltc_tmx! it does not work for prof

doc = minidom.parse(arg1)
errors = 0
restore_texts = {}
variants = 0

tus = doc.getElementsByTagName("tu") #возвращает список tu (элемента, содержащего tuvs)

# loop over all tuvs in tus to create a list of keys (=fn) in the statistics and restore_text dics; this dic has a list of values for each key
fns = []
for tu in tus:
	tuvs = tu.getElementsByTagName("tuv")
	for tuv in tuvs:
		fn = tuv.getAttribute('filesource')
		if len(fn) == 0:
			errors += 1
		fn = fn.strip()
		if fn not in fns:
			fns.append(fn)
statistics = {fn :{} for fn in fns}

# build the dic and collect all values (=text segments)
print("Number of tus: ", len(tus))

for tu in tus:
	tuvs = tu.getElementsByTagName("tuv")
	variants += len(tuvs)
	
	for tuv in tuvs:
		fn = tuv.getAttribute('filesource')
		if len(fn) == 0:
			errors += 1
		fn = fn.strip()
		seg_el = tuv.getElementsByTagName("seg")[0]
		# print(fn)
		seg_text = seg_el.childNodes[-1].data

		seg_text = seg_text.strip()
		# print seg_text
		try:
			restore_texts[fn].append(seg_text)
		except KeyError:
			restore_texts[fn] = [seg_text]

print(errors)
print("Number of tuvs: ", variants)
# writing and printing a dic is a trick

for fn, segs in restore_texts.items():
	# print(fn, '\t', len(segs), '\t', len(set(segs)))
	try:
		statistics[fn]['tuvs'].append(len(segs))
	except KeyError:
		statistics[fn]['tuvs'] = len(segs)

# produce word count for each file, which can be accessed as restore_segs[fn]

for fn, segs in restore_texts.items():
	segs = set(segs)  # пробуем удалить дубли и сократать неадекватное повторение одного и того же. Но это не вполне удастся,
	# поскольку бывает разное членение!
	# print(len(segs), '\t', len(set(segs)))
	wc = 0
	for seg in segs:
		words = len(seg.split())
		wc += words
	statistics[fn]['wc'] = wc




#запишем-ка в файл
with open("/home/masha/dialogue2018/rltc-tmx.wc", 'w') as outfile: #adjust outfile names appropriately
	writer = csv.writer(outfile, delimiter='\t')
	writer.writerow(['file'] + ['tuvs']  + ['wc'])
	for fn, nest in statistics.items():
		writer.writerow([fn] + [nest['tuvs']] + [nest['wc']]) #+ [nest['freq']]+ [nest['nfreq']])

