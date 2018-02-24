#!/usr/bin/python3

## this is a one-time effort to clean rltc.tmx
## there are three parts in this script that need to be run one after the other: each next part takes the output of the previous one
## + see part 4 (demultiplication of sources)

import sys
from xml.dom import minidom
import re

arg1 = sys.argv[1] #rltc.tmx

# produce a list of tus
doc = minidom.parse(arg1)
body = doc.childNodes[1].childNodes[3]  # equals body = doc.getElementsByTagName("body")[0]

tus = body.getElementsByTagName("tu")
print("BODY 0:", len(tus))

## PART1: filtering out offensive tus

zero_count = 0
weird = 0
poor_quality = 0
fn_lst = []

# 1) no prop at all
for tu in tus:
    props = tu.getElementsByTagName("prop")

    if len(props) == 0: # no prop at all <tu creationdate="20150317T175317Z" creationid="LF Aligner 4.1" id="20169">
        # print("ZERO PROP LENGTH")
        # num = tu.getAttribute('id')
        # print(num)
        zero_count += 1
        body.removeChild(tu)
 # 2) egypt rus-egypt angl, en-ru, eng-rus, en-rus
    elif len(props) == 1:
        prop0 = props[0]
        fn = prop0.childNodes[-1].data
        # fn_lst.append(fn)
        # print(set(fn))
        if "EN" not in fn:
            # print(fn)
            body.removeChild(tu)
            weird += 1
# 8 source files to be realigned and reintroduced to rusltc
        elif "RU_1_222-" in fn or "EN_1_202" in fn or "EN_1_227-" in fn or "EN_1_228-" in fn or "EN_1_238-" in fn \
                or "RU_1_223" in fn or "RU_1_230-" in fn or "EN_3_15-" in fn:

            body.removeChild(tu)
            poor_quality += 1
body1 = body
print("Number of zero props: ", zero_count)
print("Number of weird prop like egypt...: ", weird)
print("Number of tus from 8 source files and all their translations to be re-introduced to the RusLTC", poor_quality)

tus = body1.getElementsByTagName("tu")
print("BODY 1:", len(tus))

## Part 2: проверяем сколько осталось ошибок и удаляем отдельные tuv


# zero_type = 0
# short_st_fls = 0
# short_tt_fls = 0
#
# for tu in tus:
#     tuvs = tu.getElementsByTagName("tuv")
#     for tuv in tuvs:
#         tuv_type = tuv.getAttribute('type')
#         if len(tuv_type) == 0: # this works around empty attuibutes (type="")
#             tuv.parentNode.removeChild(tuv)
#             zero_type += 1
#         elif tuv_type == 'Source':
#             fls_st = tuv.getAttribute('filesource')
#             if len(fls_st.strip()) <= 9:  # ".head.txt":
#                 tuv.parentNode.removeChild(tuv)
#                 short_st_fls += 1
#         elif tuv_type == 'Translation':
#             fls_tt = tuv.getAttribute('filesource')
#
#             # 3) filesource = .head.txt
#             if len(fls_tt.strip()) <= 9:  # ".head.txt":
#                 tuv.parentNode.removeChild(tuv)
#                 short_tt_fls += 1
# print("Number of tuv with zero type attribute: ", zero_type)
# print("Short filesources in sources: ", short_st_fls)
# print("Short filesources in targets: ", short_tt_fls)
#
# body2 = body
#
# body2 = body
# tus = body2.getElementsByTagName("tu")
# print("BODY 2:", len(tus))
# count = 0
#
# ## Part3: different filenames in filesources of sources and targets (they are only 2, but strangely weird messed up tus)
#
# print("TUs with translations from unmatching documents")
# print("id", '\t', "num of mismatches", '\t', "clipped filenames")
# for tu in tus:
#     ID = tu.getAttribute('id')
#     tuvs = tu.getElementsByTagName("tuv")
#     bare_fls_lst = []
#     for tuv in tuvs:
#         tuv_type = tuv.getAttribute('type')
#         tuv_lang = tuv.getAttribute('xml:lang')
#         if tuv_type == 'Source': # and tuv_lang == 'EN'
#             fls_st = tuv.getAttribute('filesource')
#             fls_st_bare = re.sub(r"[A-Z]+(_\d_\d+?)\.head\.txt", r"\1", fls_st)
#             bare_fls_lst.append(fls_st_bare)
#         if tuv_type == 'Translation': #  and tuv_lang == 'RU'
#             fls_tt = tuv.getAttribute('filesource')
#             fls_tt_bare = re.sub(r"[A-Z]+(_\d_\d+?)_\d+?\.head\.txt", r"\1", fls_tt)
#             # print(fls_tt_bare)
#             bare_fls_lst.append(fls_tt_bare)
#
#
#     mess = len(set(bare_fls_lst))
#     if mess > 1:
#         body2.removeChild(tu)
#         count += 1
#         print(ID, '\t', mess, '\t', bare_fls_lst)
#
# body3 = body2
# tus = body3.getElementsByTagName("tu")
# print("I have just deleted", count, "tus with translations that come from random files, not ST translations")
#
# print("BODY 3:", len(tus))


            
        
        



# ofile = open('rltc_clean-tus.tmx','w')#the resulting cleaned (customized) tmx is in the working folder
# ofile.write(doc.toxml())
#
# ofile.close()

print("FINISHED")






