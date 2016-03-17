#/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import print_function
import subprocess
import os
import fcntl
import shlex
import sys

# command = 'java -mx2048m -cp "%s": edu.stanford.nlp.parser.lexparser.LexicalizedParser -sentences newline -tokenized -escaper edu.stanford.nlp.process.PTBEscapingProcessor -outputFormat wordsAndTags,penn,typedDependenciesCollapsed -outputFormatOptions basicDependencies "%s" -' % (parser_path, model_path)

def _convert_result_to_list(result):
    def parse_token(token):
        # find the last index of '/'
        i = token.rindex('/')
        return token[:i], token[i+1:]
    return map(parse_token, result.decode('utf-8').split())

def _parse_wrapper(tagger):
    def __wrapper(self, text, raw=False):
        text = text.strip()
        if not text:
            return b'' if raw else ''
        if '\n' in text:
            raise Exception('newline in input')

        result = tagger(self, text)

        if raw:
            return result.strip()
        else:
            res = _convert_result_to_list(result)
            if res[-1][1] == res[-2][1]:
                return res[:-1]
            else:
                return res
    return __wrapper

class StanfordTagger:

    @staticmethod
    def set_nonblock_read(output):
        fd = output.fileno()
        fl = fcntl.fcntl(fd, fcntl.F_GETFL)
        fcntl.fcntl(fd, fcntl.F_SETFL, fl | os.O_NONBLOCK)

    def __init__(self, path_to_tagger, arguments=[]):
        DEVNULL = open(os.devnull, 'wb')
        # outputFormat: wordsAndTags, penn, typedDependencies
        args = shlex.split('-mx150m -cp ./* edu.stanford.nlp.parser.lexparser.LexicalizedParser -sentences newline -outputFormat wordsAndTags edu/stanford/nlp/models/lexparser/englishPCFG.ser.gz -')
        self._tagger = subprocess.Popen(['java'] + args,
                                        cwd=path_to_tagger,
                                        stdin=subprocess.PIPE,
                                        stdout=subprocess.PIPE,
                                        stderr=DEVNULL)
        StanfordTagger.set_nonblock_read(self._tagger.stdout)

    @_parse_wrapper
    def parse(self, text):
        # add ' .' so that stanford parser always considered the end of a sentence
        self._tagger.stdin.write((text + '\n').encode('utf-8'))
        self._tagger.stdin.flush()

        result = ''
        while True:
            try:
                result += self._tagger.stdout.read()
            except:
                continue
            if result and result[-2:] == b'\n\n':
                break
        return result.strip()
