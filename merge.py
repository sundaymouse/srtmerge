#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#Subtitle Multi-line Merge
#Copyright (c) sundaymouse 2014
#License: GNU GENERAL PUBLIC LICENSE, Version 3, 29 June 2007.
#For full license details, see: http://www.gnu.org/copyleft/gpl.html
#
#THERE IS NO WARRANTY FOR THE PROGRAM, TO THE EXTENT PERMITTED BY APPLICABLE LAW. 
#EXCEPT WHEN OTHERWISE STATED IN WRITING THE COPYRIGHT HOLDERS AND/OR OTHER PARTIES PROVIDE THE PROGRAM “AS IS” WITHOUT WARRANTY OF ANY KIND, 
#EITHER EXPRESSED OR IMPLIED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE. 
#THE ENTIRE RISK AS TO THE QUALITY AND PERFORMANCE OF THE PROGRAM IS WITH YOU. SHOULD THE PROGRAM PROVE DEFECTIVE, 
#YOU ASSUME THE COST OF ALL NECESSARY SERVICING, REPAIR OR CORRECTION.
#
#Purpose of the script:
#Some closed caption subtitle files contain multiple lines of subtitle in a single subtitle timing block.
#This script merges multiple lines into a single line. If Non-English translation lines are also present,
#they will be seperately merged into another line, on top of the English line.
#We use Chinese as the intended translated language. This script may not apply to some languages with the same charset to English.
#
#Rules of detecting and merging:
#Empty lines will be stripped at the start, only to be replaced at the end of operations.
#Lines containing all of comma, ":" and "-->" will be treated as a time line;
#Otherwise, all lines containing Chinese characters, symbols or punctuations will be treated as a Chinese line;
#Otherwise, any pure-number line directly above "-->" will be treated as srt line number, otherwise it will be treated as an English line;
#Otherwise, a line will be treated as an English line.
#
#All English lines in a block are merged together, and so do the Chinese lines.
#A space is always added to between two merging lines.

import sys
import os

EnglishLineCharset = list("ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz1234567890.,''""?!:;-—()$ ") 
#If a character or symbol is not in this charset, they will be moved to a seperated translated line. Change the charset if you wish.

InputFileName = sys.argv[1]
OutputFileName = sys.argv[2]
LineList = []
SubtitleList = []
OutputBlockList = []
WriteList = []

if os.path.exists(OutputFileName):
	OverwriteChoice = raw_input("Output target file exists, overwrite? [y/n]:")
	if OverwriteChoice != "y":
		sys.exit("Not overwriting file, aborted.")
	else:
		print "Overwriting",OutputFileName,"..."

print "Reading from",InputFileName, "."

try:
	srtfile = file(InputFileName, 'r')
except:
	sys.exit("File cannot be opened, check if file path is correct.")

while True:
	CurrentLine = srtfile.readline()
	if len(CurrentLine) == 0:
		break
	else:
		LineList.append(CurrentLine.rstrip().decode('utf-8-sig'))
srtfile.close()

try:
	outfile = file(OutputFileName, 'w')
except:
	sys.exit("Fail to create output file, check if your path is valid.")


#Remove all lines with only spaces or just empty first
i = 0
while i < len(LineList):
	if (LineList[i].replace(' ', '') == ''):
		LineList.remove(LineList[i])
		i = i - 1
	i = i + 1


#Group lines by judging if there's a number above a timer line.
lineno = 0
NewBlock = []

while lineno < len(LineList):
	try:
		int(LineList[lineno]) #Fail if it's not a srt line number, just add the line to current block, as in "except ValueError"
		if ("-->" in LineList[lineno+1]) and (":" in LineList[lineno+1]) and ("," in LineList[lineno+1]):
			SubtitleList = SubtitleList + [NewBlock]
			NewBlock = [LineList[lineno]]
	except ValueError:
		NewBlock.append(LineList[lineno])
	if lineno == len(LineList) - 1:
		SubtitleList = SubtitleList + [NewBlock] #To save the final block into SubtitleList
	lineno = lineno + 1

SubtitleList.pop(0) #Remove the first empty block from SubtitleList.


#Merge Chinese and English lines
for block in SubtitleList:
	elementno = 2 #the first and second element in the block are srt line number and srt timer, don't need them
	ChineseSubLine = ''
	EnglishSubLine = ''
	while elementno < len(block):
		if set(block[elementno]).issubset(EnglishLineCharset):
			if EnglishSubLine == '':
				EnglishSubLine = block[elementno] #To prevent a space at the beginning of a line.
			else:
				EnglishSubLine = EnglishSubLine + ' ' + block[elementno]
		else:
			if ChineseSubLine == '':
				ChineseSubLine = block[elementno] #To prevent a space at the beginning of a line.
			else:
				ChineseSubLine = ChineseSubLine + ' ' + block[elementno]
		elementno = elementno + 1
	if ChineseSubLine != '': #If a block does not contain chinese characters or symbols, don't add a chinese subtitle line
		OutputBlockList = OutputBlockList + [block[0], '\n', block[1], '\n', ChineseSubLine, '\n', EnglishSubLine, '\n', '\n']
	else:
		OutputBlockList = OutputBlockList + [block[0], '\n', block[1], '\n', EnglishSubLine, '\n', '\n',]


#Write to output file
print "Writing to",OutputFileName,"."
for item in OutputBlockList:
	outfile.write(item.encode('utf-8'))
outfile.close()





