#!/usr/bin/python3

import os, os.path
import sys
import subprocess
from xml.sax.saxutils import escape

class Reader():
    def __init__(self, out):
        self.out = out

    def startswith(self, string):
        if self.out.startswith(string):
            self.out = self.out[len(string):]
            return True
        else:
            return False

    def ignoreLine(self):
        i = self.out.find("\n")
        if i == -1:
            self.out = ""
        else:
            self.out = self.out[i:].lstrip()

    def readString(self):
        i = self.out.find('"')
        if i == -1:
            raise Exception("String Not Found")
        j = self.out.find('"', i+1)
        if j == -1:
            raise Exception("Not terminating string")
        res = self.out[i+1:j]
        self.out = self.out[j:]
        self.ignoreLine()
        return escape(res)

    def readList(self):
        things = []
        while not self.startswith("]"):
            things.append(self.readString())
        self.ignoreLine()
        return things

    def read(self):
        self.out = self.out.lstrip()
        c = self.out[0]
        if c == '"':
            return (self.readString(),)
        elif c == "[":
            self.out = self.out[1:].lstrip()
            return self.readList()
        else:
            raise Exception("Unsupported datatype: %s" % c)

def NotStarted():
    raise Exception("`name` tag not found.")

def main():
    pkgname = os.path.basename(os.path.abspath("."))
    # pkgname = "coq-hammer.1.1+8.9"
    out = subprocess.getoutput('opam show --raw "%s"' % pkgname)
    r = Reader(out)
    started = False
    while r.out:
        if r.startswith("name: "):
            started = True
            name = r.readString()
            print('<!-- XML HEADERS HERE -->')
            print('<Package Name="%s">' % name)
        elif r.startswith("synopsis: "):
            if not started: NotStarted()
            data = r.readString()
            print('  <Synopsis>%s</Synopsis>' % data)
        elif r.startswith("homepage: "):
            if not started: NotStarted()
            data = r.readString()
            print('  <Homepage>%s</Homepage>' % data)
        elif r.startswith("license: "):
            if not started: NotStarted()
            data = r.readString()
            print('  <License>%s</License>' % data)
        elif r.startswith("version: "):
            if not started: NotStarted()
            data = r.readString()
            print('  <Version>%s</Version>' % data)
        elif r.startswith("tags: "):
            if not started: NotStarted()
            data = r.read()
            for tag in data:
                tagg = tag.split(":")
                if len(tagg) == 2:
                    if tagg[0] == "category":
                        print('  <Category>%s</Category>' % tagg[1])
                    elif tagg[0] == "keyword":
                        print('  <Keyword>%s</Keyword>' % tagg[1])
        elif r.startswith("authors: "):
            if not started: NotStarted()
            entries = r.read()
            for entry in entries:
                print('  <Author>%s</Author>' % entry)
        elif r.startswith("depends: "):
            if not started: NotStarted()
            entries = r.read()
            for entry in entries:
                print('  <Depends>%s</Depends>' % entry)
        else:
            r.ignoreLine()
    if started:
        print('</Package>')

if __name__ == "__main__":
    main()
