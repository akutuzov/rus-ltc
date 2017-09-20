#!/usr/bin/python2
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

    print >> sys.stderr, 'Parsing the base TMX...', oldtmxfile
    oldtmx = minidom.parse(oldtmxfile)

    oldbody = oldtmx.getElementsByTagName("body")[0]

    old_translation_units = oldtmx.getElementsByTagName('tu')
    print >> sys.stderr, len(old_translation_units), 'translation units found.'
    print >> sys.stderr, 'Validating...'

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
            print >> sys.stderr, 'The base TMX contains non-unique IDs! Stopping.'
            exit()
        else:
            ids.add(tu_id)

        existing[(filesource, segment.firstChild.data.strip())] = tu.getAttribute('id')

    old_translation_units = oldtmx.getElementsByTagName("tu")
    print >> sys.stderr, 'TUs with empty source segments or lacking source metadata removed from the base TMX:', empty
    print >> sys.stderr, len(old_translation_units), 'translation units after validation.'

    print >> sys.stderr, "====="
    print >> sys.stderr, "Parsing new TMX...", newtmxfile + '.tmx'
    newtmx = minidom.parse(newtmxfile + '.tmx')

    translation_units = newtmx.getElementsByTagName("tu")
    print >> sys.stderr, len(translation_units), 'translation units found.'
    print >> sys.stderr, 'Enriching new TMX with meta data...'
    errors = 0

    for tu in translation_units:
        props = tu.getElementsByTagName("prop")
        if len(props) == 1:
            props = props[0]
        else:
            print >> sys.stderr, 'TU without file sources detected and deleted!'
            print >> sys.stderr, tu.getAttributeNode('changeid').nodeValue.strip()
            print >> sys.stderr, tu.getAttributeNode('changedate').nodeValue.strip()
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
            print >> sys.stderr, 'Header not found for', source
            print >> sys.stderr, 'Stopping.'
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
    print >> sys.stderr, 'Errors:', errors
    print >> sys.stderr, len(translation_units), 'translation units in the new TMX after validation.'
    print >> sys.stderr, "====="

    print >> sys.stderr, 'Adding new TUs to the base TMX...'

    counter = max(ids)
    for tu in translation_units:
        tuvs = tu.getElementsByTagName("tuv")
        (tuv_source, tuv_target) = tuvs
        segment = tuv_source.getElementsByTagName("seg")[0]
        filesource = tuv_source.getAttribute('filesource')

        if (filesource, segment.firstChild.data.strip()) in existing:
            existing_tu_id = existing[(filesource, segment.firstChild.data.strip())]
            print >> sys.stderr, 'Found matching source in the base TMX at the id', existing_tu_id
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
    print >> sys.stderr, len(old_translation_units), 'translation units in the resulting TMX.'

    newfilename = 'rltc_' + newtmxfile + '.tmx'
    with codecs.open(newfilename, 'w', 'utf-8') as f:
        f.write(oldtmx.toxml())
    print >> sys.stderr, 'New TMX saved to', newfilename


if __name__ == '__main__':
    main()
