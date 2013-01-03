#!/usr/bin/env python
import sys, os

inputfile = sys.argv[1]
outputfile = sys.argv[1] + "joined.svg"

#EditSelectAll
#SelectionUnion

cmd = "inkscape " + inputfile + " --verb=EditSelectAll --verb=SelectionUnion --verb=FileSave --verb=FileQuit"
#cmd = "inkscape " + inputfile + " --verb=EditSelectAll --verb=SelectionUnion --export-plain-svg=" + outputfile
print cmd
os.system(cmd)


