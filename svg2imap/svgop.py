
#!/usr/bin/python

import sys
import xml.etree.ElementTree as ET

prop = ""
oldValue = ""
newValue = ""

matches = []

def getStylesheet(node):
	"""
		retrieve the stylesheet (value of the style attr) of a given node
		and return a dictionary of properties and their values
	"""
	styledict = {}
	stylesheet = node.attrib.get("style")
	stylesheet = stylesheet.split(";")

	# fix for single line styles that end with a semicolon
	if len(stylesheet) > 1 and stylesheet[1] == "":
		stylesheet[0] = stylesheet[0] + ";"
		stylesheet.pop(1)

	# now cycle through the list and populate the stylesheet dictionary
	for style in stylesheet:
		if style: # needed?
			attr = style.split(":")[0]
			value = style.split(":")[1]
			styledict[attr] = value
	return styledict

def setStylesheet(node,styledict):
	"""
	sets a new value for a node's style attr given a stylesheet
	"""
	attr = styledict2attr(styledict)
	node.set("style", attr)

def styleReplace(styledict, prop, oldValue, newValue):
	"""
	accepts a stylesheet dictionary and changes values according
	to input
	"""
	# check against 4 possible scenarios - either prop
	# or oldValue can be a string or a list

	if isinstance(prop, str) and isinstance(oldValue, str):
		for key in styledict:
			# is it a match?
			if key == prop and styledict[key] == oldValue:
				styledict[key] = newValue

	elif isinstance(prop, list) and isinstance(oldValue, str):
		for key in styledict:
			for item in prop:
				if key == item and styledict[key] == oldValue:
					styledict[key] = newValue

	elif isinstance(prop, str) and isinstance(oldValue, list):
		for key in styledict:
			for value in oldValue:
				if key == prop and styledict[key] == value:
					styledict[key] = newValue

	elif isinstance(prop, list) and isinstance(oldValue, list):
		for key in styledict:
			for item in prop:
				for value in oldValue:
					if key == item and styledict[key] == value:
						styledict[key] = newValue
	return styledict

def parseNode(node):
    return getPathData(node)
        
def getPathData(node):
    tag = str(node.tag.split('}')[1])
    id = str(node.attrib.get('id'))
    data = node.attrib.get('d')
    if tag == 'path' and not id.startswith('path'):
        return (id, data)

'''
# this was used for style replacement

def parseNode (node,prop,oldValue,newValue):
	# does it have the style attribute?
	if node.attrib.get("style"):
		# get its stylesheet
		stylesheet = getStylesheet(node)
		# act on it
		newstyle = styleReplace(stylesheet, prop, oldValue, newValue)
		setStylesheet(node, newstyle)
'''

def styledict2attr(styledict):
	"""
	Converts a stylesheet dict to a single string (as per SVG syntax)
	"""
	pairs = []
	for key in styledict:
		pairs.append(key + ":" + styledict[key])
	attr = ';'.join(pairs)
	return attr

def traverseNode(node):
	"""
	Recursively checks each node
	"""
	global matches
	for child in node:
		m = parseNode(child)
		if m:
		    matches.append(m)
		# does this node have children? if so, check them too
		if len(child) > 0:
			traverseNode(child)

def traverseTree(tree):
    global matches
    root = tree.getroot()
    for node in root:
	    traverseNode(node)
    return matches

def openTree(file):
	tree = ET.parse(file)
	return tree

def saveTree(tree, outfile):
	tree.write(outfile)

def main(filename):
	tree = openTree(filename)
	traverseTree(tree)
	# saveTree(tree, outfile)

if __name__ == "__main__":
    import sys
    main(sys.argv[1])
	
