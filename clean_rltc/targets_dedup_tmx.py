#!/usr/bin/python3

## Part 5 (deduplicate targets) of Feb 2018 rltc.tmx cleaning effort

import sys
from xml.dom import minidom


arg1 = sys.argv[1] #rltc.tmx

doc = minidom.parse(arg1)
body = doc.childNodes[1].childNodes[3]

tus = body.getElementsByTagName("tu")
print("BODY 0:", len(tus))

# make lists of tuvs in each tu and test whether each tuv is in it (based on segs filesource), else delete tuv and print tu's ID and duplicate seg
count = 0
alltuvs = 0
badfiles = []

for tu in tus:
	segs = []
	filesources = []
	ID = tu.getAttribute("id")
	tuvs = tu.getElementsByTagName("tuv")
	for tuv in tuvs:
		alltuvs += 1
		fls = tuv.getAttribute('filesource')
		fls = fls.strip()
		segment = tuv.getElementsByTagName("seg")[0]
		seg_text = segment.childNodes[-1].data
		seg_text = seg_text.strip()

		if fls not in filesources and seg_text not in segs:
			filesources.append(fls)
			segs.append(seg_text)
		elif seg_text in segs and fls in filesources:
			tuv.parentNode.removeChild(tuv)
			# print(seg_text)
			badfiles.append(fls)
			count += 1
for fls in set(badfiles):
	print(fls)
	
print("Number of targets which have duplicate segments in rltc.tmx :", len(set(badfiles)))

body1 = body
tuvs = body1.getElementsByTagName("tuv")

print("BODY0 number of tuvs: ", alltuvs)
print("BODY1-tuvs deleted: ", count, "remaining: ", len(tuvs))

ofile = open('rltc_targets_dedupped.tmx','w') # the resulting cleaned (customized) tmx is in the working folder
ofile.write(doc.toxml())

ofile.close()

print("FINISHED")
