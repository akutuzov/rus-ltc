#! python
# coding: utf-8

import json
import sys
from xml.dom import minidom
import requests

PORT = 66666


def tag_ud(words):
    # UDPipe tagging for any language you have a model for.
    # Demands UDPipe REST server (https://ufal.mff.cuni.cz/udpipe/users-manual#udpipe_server)
    # running on a port defined in webvectors.cfg
    # Start the server with something like:
    # udpipe_server --daemon 66666 MyModel MyModel /opt/my.model UD

    # Sending user query to the server:
    ud_reply = requests.post('http://localhost:%s/process' % PORT,
                             data={'tokenizer': '', 'tagger': '', 'data': words}).content

    # Getting the result in the CONLLU format:
    processed = json.loads(ud_reply.decode('utf-8'))['result']

    # Skipping technical lines:
    content = [l for l in processed.split('\n') if not l.startswith('#')]

    content = [w.split('\t') for w in content if len(w) > 1]

    # Extracting lemmas and tags from the processed queries:
    tagged = [(w[1], w[2], w[3]) for w in content if w]

    # poses = [t.split('_')[1] for t in tagged]
    return tagged


lang = 'EN'

wordforms = {}

tmxfile = sys.argv[1]

tmx = minidom.parse(tmxfile)

body = tmx.getElementsByTagName("body")[0]

translation_units = tmx.getElementsByTagName('tu')

for tu in translation_units:
    tuvs = tu.getElementsByTagName("tuv")
    for tuv in tuvs:
        language = tuv.getAttribute('xml:lang')
        if language == lang:
            segment = tuv.getElementsByTagName("seg")[0]
            text = segment.childNodes[0].data
            lemmatized = tag_ud(text)
            for el in lemmatized:
                (token, lemma, pos) = el
                if token not in wordforms:
                    wordforms[token] = set()
                parsing = (lemma, pos)
                wordforms[token].add(parsing)

for token in wordforms:
    parsings = ['<ana lex = "%s", gr = "%s"></ana>' % (p[0], p[1]) for p in wordforms[token]]
    parsings = ''.join(parsings)
    out = '<w>%s%s</w>' % (parsings, token)
    print(out)
