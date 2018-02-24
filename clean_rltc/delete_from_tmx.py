#!/usr/bin/python3
# coding: utf-8

# get rid of unwanted files = clean tmx

import sys
from xml.dom import minidom


arg1 = sys.argv[1] #rltc.tmx

doc = minidom.parse(arg1)
body = doc.childNodes[1].childNodes[3]

tus = body.getElementsByTagName("tu")
print("BODY 0:", len(tus))

count = 0
zero_count = 0
other = 0
# find and delete tu with no prop at all
# for tu in tus:
#     props = tu.getElementsByTagName("prop")
#
#     if len(props) == 0: # no prop at all <tu creationdate="20150317T175317Z" creationid="LF Aligner 4.1" id="20169">
#         # print("ZERO PROP LENGTH")
#         # num = tu.getAttribute('id')
#         # print(num)
#         zero_count += 1
#         body.removeChild(tu)
#  # 2) egypt rus-egypt angl, en-ru, eng-rus, en-rus
#     elif len(props) == 1:
#         prop0 = props[0]
#         fn = prop0.childNodes[-1].data
#         # deleted earlier RU_4_21 EN_3_15 RU_6_19 EN_1_105 EN_4_18
#         if "EN_4_17" in fn:
#             # print(fn)
#             body.removeChild(tu)
#             other += 1
#             continue
# body1 = body
# print(zero_count, other)
# tus = body1.getElementsByTagName("tu")
# print("BODY 1:", len(tus))


for tu in tus:
    tuvs = tu.getElementsByTagName("tuv")
    for tuv in tuvs:
        fls = tuv.getAttribute('filesource')
        # неполный список удаленных из tmx файлов RU_4_33_1.head.txt, RU_1_102_12.head.txt, RU_4_39_1.head.txt, RU_3_14_2.head.txt

        if fls == 'EN_1_149_13.head.txt' :
            tuv.parentNode.removeChild(tuv)
            count += 1


print("BODY 1-tuvs: ", count)

ofile = open('rltc_deleted.tmx','w')#the resulting cleaned (customized) tmx is in the working folder
ofile.write(doc.toxml())

ofile.close()

print("FINISHED")
