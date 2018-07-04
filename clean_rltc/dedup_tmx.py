#!/usr/bin/python3

## Part 4 of Feb 2018 rltc.tmx cleaning effort: дедуплицируем оригиналы - привязываем множественные переводы к одному и тому же сегменту
# работает по принципу переливания содержания tmx через сито в пустую память
# этот скрипт надо запускать после tmx_update.py для консолидации всех переводов новых оригиналов

# Usage: ./dedup_tmx.py -old empty_rltc.tmx -new rltc2deduplicate.tmx

import sys, os
from xml.dom import minidom
import re
import argparse


parser = argparse.ArgumentParser()
parser.add_argument("-old", help="Base (old) TMX file", required=True)
parser.add_argument("-new", help="New TMX file", required=True)
args = parser.parse_args()

oldtmxfile = args.old
newtmxfile = args.new

existing = {}

print('Parsing the base TMX...', oldtmxfile, file=sys.stderr)
oldtmx = minidom.parse(oldtmxfile)

oldbody = oldtmx.getElementsByTagName("body")[0]

old_translation_units = oldtmx.getElementsByTagName('tu')
print(len(old_translation_units), 'translation units found.', file=sys.stderr)


for old_tu in old_translation_units:
	tuvs = old_tu.getElementsByTagName("tuv")
	for tuv in tuvs:
		tuv_type = tuv.getAttribute('type')
		if tuv_type == 'Source':
			tuv_source = tuv
			break
	segment = tuv_source.getElementsByTagName("seg")[0]
	filesource = tuv_source.getAttribute('filesource')
	existing[(filesource, segment.firstChild.data.strip())] = old_tu.getAttribute('id')

print("=====", file=sys.stderr)
print("Parsing new TMX...", newtmxfile, file=sys.stderr)
newtmx = minidom.parse(newtmxfile)
translation_units = newtmx.getElementsByTagName("tu")
print(len(translation_units), 'translation units found.', file=sys.stderr)
counter = 0

for tu in translation_units:
	tuvs = tu.getElementsByTagName("tuv")
	targets = []
	for tuv in tuvs:
		tuv_type = tuv.getAttribute('type')
		if tuv_type == 'Source':
			fls_st = tuv.getAttribute('filesource')
			fls_st_bare = re.sub(r"[A-Z]+(_\d_\d+?)\.head\.txt", r"\1", fls_st)
			seg_el = tuv.getElementsByTagName("seg")[0]
			seg_text = seg_el.childNodes[-1].data
			seg_text = seg_text.strip()
			# print("ST: ", seg_text)
	
	# 	# a dictionary with tuples as keys and IDs as values
	# 	# проходим по всему корпусу, создаем словарь уникальных сегментов оригинала и переписываем их в пустую память
	if (fls_st, seg_text) not in existing.keys():
		existing[(fls_st, seg_text)] = tu.getAttribute('id') # обновляем словарь
		toadd = oldtmx.importNode(tu, True)
		oldbody.appendChild(toadd)
		counter += 1
print("I have added", counter, "tus with uniq sources from the 'existing' dic")
print("======================================================")

# заново читаем tmx и сравниваем сегменты оригинала с existing, отыскивая совпадения без тождества имен файлов.
oldbody2 = oldbody
old_translation_units2 = oldbody2.getElementsByTagName('tu')
print("Size of new TMX in tus with uniq source segs: ", len(old_translation_units2)) # ожидаем 5

added_targets = 0

for tu in translation_units:
	tuvs = tu.getElementsByTagName("tuv")
	ID = tu.getAttribute("id")
	for tuv in tuvs:
		tuv_type = tuv.getAttribute('type')
		if tuv_type == 'Source':
			fls_st = tuv.getAttribute('filesource')
			fls_st_bare = re.sub(r"[A-Z]+(_\d_\d+?)\.head\.txt", r"\1", fls_st)
			seg_el = tuv.getElementsByTagName("seg")[0]
			seg_text = seg_el.childNodes[-1].data
			seg_text = seg_text.strip()
		
		if (fls_st, seg_text) in existing.keys() and ID != existing[(fls_st, seg_text)]:
			existing_tu_id = existing[(fls_st, seg_text)] # установили номер сегмента, в который будем добавлять множественные переводы из обрабатываемого tu
		
			if tuv_type == 'Translation':
				tuv_target = tuv
				fls_tt = tuv.getAttribute('filesource')
				fls_tt_bare = re.sub(r"[A-Z]+(_\d_\d+?)_\d+?\.head\.txt", r"\1", fls_tt)
				for old_tu2 in old_translation_units2:
					if old_tu2.getAttribute("id") == existing_tu_id: # находим тот, который по оригиналу совпадает с обрабатываемым
						if fls_tt_bare == fls_st_bare: # предотвращаем случайные совпадения между разными оригиналами = у переводов должна быть та же база в имени
							toadd = oldtmx.importNode(tuv_target, True)
							old_tu2.appendChild(toadd)
							added_targets += 1

oldbody3 = oldbody2
old_translation_units3 = oldbody3.getElementsByTagName('tu')
# print("Number of tus does not change: ", len(old_translation_units3)) # ожидаем 5 на тестовом материале
print("Number of added multiple targets: ", added_targets) # ожидаем 6

ofile = open('dedup_rltc.tmx','w')
ofile.write(oldtmx.toxml())

ofile.close()

print("FINISHED")
