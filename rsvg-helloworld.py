#!/usr/bin/env python

import rsvg

svg = rsvg.Handle('output.svg')
for prop in svg.props:
    print prop
    
print svg.props.width, svg.props.height
