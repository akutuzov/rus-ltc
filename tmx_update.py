#!/usr/bin/python3
# coding: utf-8
import codecs
import os
import sys
from xml.dom import minidom
import argparse

"""
Takes as an input the base TMX file and a file with the new batch.
Directory containing all the headers should be present and bear the name identical to the name of the new batch file.
For example:
batch17/
batch17.tmx

Arguments:
-old <file> Base (old) TMX file
-new <file> New TMX file

Example:
./tmx_update.py -old rltc.tmx -new batch17

"""


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-old", help="Base (old) TMX file", required=True)
    parser.add_argument("-new", help="New TMX file", required=True)
    args = parser.parse_args()

    oldtmxfile = args.old
    newtmxfile = args.new

    attributes = ['gender', 'experience', 'mark', 'stage', 'genre', 'stress', 'conditions', 'year', 'type',
                  'affiliation']

    existing = {}
    empty = 0
    ids = set()

    print('Parsing the base TMX...', oldtmxfile, file=sys.stderr)
    oldtmx = minidom.parse(oldtmxfile)

    oldbody = oldtmx.getElementsByTagName("body")[0]

    old_translation_units = oldtmx.getElementsByTagName('tu')
    print(len(old_translation_units), 'translation units found.', file=sys.stderr)
    print('Validating...', file=sys.stderr)

    for tu in old_translation_units:
        tuvs = tu.getElementsByTagName("tuv")
        for tuv in tuvs:
            tuv_type = tuv.getAttribute('type')
            if tuv_type == 'Source':
                tuv_source = tuv
                break
        segment = tuv_source.getElementsByTagName("seg")[0]
        filesource = tuv_source.getAttribute('filesource')
        if len(segment.childNodes) == 0 or filesource.strip() == ".head.txt":
            oldbody = tu.parentNode
            oldbody.removeChild(tu)
            empty += 1
            continue
        tu_id = int(tu.getAttribute('id'))
        if tu_id in ids:
            print('The base TMX contains non-unique IDs! Stopping.', file=sys.stderr)
            exit()
        else:
            ids.add(tu_id)

        existing[(filesource, segment.firstChild.data.strip())] = tu.getAttribute('id')

    old_translation_units = oldtmx.getElementsByTagName("tu")
    print('TUs with empty source segments or lacking source metadata removed from the base TMX:', empty, file=sys.stderr)
    print(len(old_translation_units), 'translation units after validation.', file=sys.stderr)

    print("=====", file=sys.stderr)
    print("Parsing new TMX...", newtmxfile + '.tmx', file=sys.stderr)
    newtmx = minidom.parse(newtmxfile + '.tmx')

    translation_units = newtmx.getElementsByTagName("tu")
    print(len(translation_units), 'translation units found.', file=sys.stderr)
    print('Enriching new TMX with meta data...', file=sys.stderr)
    errors = 0

    for tu in translation_units:
        props = tu.getElementsByTagName("prop")
        if len(props) == 1:
            props = props[0]
        else:
            print('TU without file sources detected and deleted!', file=sys.stderr)
            print(tu.getAttributeNode('changeid').nodeValue.strip(), file=sys.stderr)
            print(tu.getAttributeNode('changedate').nodeValue.strip(), file=sys.stderr)
            newbody = tu.parentNode
            newbody.removeChild(tu)
            errors += 1
            continue

        files = props.childNodes[-1].data.strip()
        (source, target) = files.split('-')
        tuvs = tu.getElementsByTagName("tuv")
        (tuv_source, tuv_target) = tuvs

        tuv_source.setAttribute('filesource', source + '.head.txt')
        tuv_target.setAttribute('filesource', target + '.head.txt')

        if not os.path.isfile(os.path.join(newtmxfile, source + '.head.txt')):
            print('Header not found for', source, file=sys.stderr)
            print('Stopping.', file=sys.stderr)
            exit()
        source_metafile = open(os.path.join(newtmxfile, source + '.head.txt')).readlines()
        target_metafile = open(os.path.join(newtmxfile, target + '.head.txt')).readlines()
        if len(source_metafile) == 9:
            source_metafile.append('\n')
        if len(target_metafile) == 9:
            target_metafile.append('\n')
        source_meta = {}
        target_meta = {}
        for attr in attributes:
            source_meta[attr] = source_metafile[attributes.index(attr)].strip()
            target_meta[attr] = target_metafile[attributes.index(attr)].strip()
        for attr in source_meta:
            if source_meta[attr]:
                tuv_source.setAttribute(attr, source_meta[attr])
            else:
                tuv_source.setAttribute(attr, '')

        for attr in target_meta:
            if target_meta[attr]:
                tuv_target.setAttribute(attr, target_meta[attr])
            else:
                tuv_target.setAttribute(attr, '')

    translation_units = newtmx.getElementsByTagName("tu")
    print('Errors:', errors, file=sys.stderr)
    print(len(translation_units), 'translation units in the new TMX after validation.', file=sys.stderr)
    print("=====", file=sys.stderr)

    print('Adding new TUs to the base TMX...', file=sys.stderr)

    counter = max(ids)
    for tu in translation_units:
        tuvs = tu.getElementsByTagName("tuv")
        (tuv_source, tuv_target) = tuvs
        # print "Still working", tuv_source
        segment = tuv_source.getElementsByTagName("seg")[0]
        # print type(segment)

        filesource = tuv_source.getAttribute('filesource')

        # find id of the offending tu in new tmx that produces the error --- AttributeError: 'NoneType' object has no attribute 'data'

        print(filesource)

        if (filesource, segment.firstChild.data.strip()) in existing:

            existing_tu_id = existing[(filesource, segment.firstChild.data.strip())]
            print('Found matching source in the base TMX at the id', existing_tu_id, file=sys.stderr)
            for old_tu in old_translation_units:
                if old_tu.getAttribute('id') == existing_tu_id:
                    toadd = oldtmx.importNode(tuv_target, True)
                    old_tu.appendChild(toadd)
        else:
            counter += 1
            tu.setAttribute('id', str(counter))
            toadd = oldtmx.importNode(tu, True)
            oldbody.appendChild(toadd)

    old_translation_units = oldtmx.getElementsByTagName("tu")
    print(len(old_translation_units), 'translation units in the resulting TMX.', file=sys.stderr)

    newfilename = 'rltc_' + newtmxfile + '.tmx'
    with codecs.open(newfilename, 'w', 'utf-8') as f:
        f.write(oldtmx.toxml())
    print('New TMX saved to', newfilename, file=sys.stderr)


if __name__ == '__main__':
    main()
