#!/Library/Frameworks/Python.framework/Versions/2.6/Resources/Python.app/Contents/MacOS/Python

# Python module for form-sensitive transitional probability analysis of harmonic structures in corpora of songs/movements

# Copyright (C) 2012 Kris P. Shaffer

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import csv
import sys
import os

class Chord():

	def __init__(self):
		self.data = []

	root = ''
	quality = '' 
	module = '' 
	lastChordInPhrase = '0' # options are 0 (no) and 1 (yes)
	lastChordInModule = '0' # options are 0 (no) and 1 (yes)
	nextRoot = ''
	nextQuality = ''
	
	
class SongAnalysis():

	def __init__(self, analysisFileName):
		self.data = []
		self.analysisFileName = analysisFileName
		self.analysisExpanded = []

	def analysisOriginal(self):
		file = csv.reader(open(self.analysisFileName, 'rb'), delimiter=',')
		analysisByModule = []
		analysisByModule.extend(file)
		return analysisByModule

	def modules(self):
	
		self.modules = []
		for chord in self.analysisOriginal():
			self.modules.append(chord[0])
		return sorted(set(self.modules))

	def chordFunctions(self):
		
		chordFunctions = []
		for chordTransition in self.expandChords():
			if chordTransition[1] != '|':
				if chordTransition[1] != '||':
					chordFunctions.append(chordTransition[1])
		return sorted(set(chordFunctions))
		
	def expandChords(self):
	
		moduleHarmoniesList = []
		
		# parse chords and put into temp file
		
		for row in self.analysisOriginal():
			moduleName = row[0]
			chordIteration = 1
			
			while chordIteration != len(row):
				
				chord = Chord()
				chord.module = moduleName
				chord.root = row[chordIteration]
				if chordIteration + 1 != len(row):
					if row[chordIteration + 1] == '|':
						chord.lastChordInPhrase = 1
					if row[chordIteration + 1] == '||':
						chord.lastChordInPhrase = 1
						chord.lastChordInModule = 1
		
				chordTempList = [chord.module,chord.root,chord.lastChordInPhrase,chord.lastChordInModule]
				moduleHarmoniesList.append(chordTempList)
				chordIteration = chordIteration + 1
		
	# create list to hold final data
	
		songHarmonies = []
	
	# take chords, add info to chords about following chords and write to list
		
		iter = 0
		totalHarmonies = len(moduleHarmoniesList)
		
		while iter != totalHarmonies:
			for tempHarmony in moduleHarmoniesList:
					chord = Chord()
					chord.module = tempHarmony[0]
					chord.root = tempHarmony[1]
					chord.lastChordInPhrase = tempHarmony[2]
					chord.lastChordInModule = tempHarmony[3]
					if iter + 1 < totalHarmonies:
						nextChord = moduleHarmoniesList[iter + 1]
					else:
						nextChord = ['','none','','']
					if iter + 2 < totalHarmonies:
						nextNextChord = moduleHarmoniesList[iter + 2]
					else:
						nextNextChord = ['','none','','']
					if nextChord[1] == '|':
						chord.nextRoot = nextNextChord[1]
					elif nextChord[1] == '||':
						chord.nextRoot = nextNextChord[1]
					else:
						chord.nextRoot = nextChord[1]
					
					if chord.root != '|':
						if chord.root != '||':
							songHarmonies.append([chord.module,chord.root,chord.nextRoot,chord.lastChordInPhrase,chord.lastChordInModule])
					iter = iter + 1
		
		return songHarmonies
	
	def chordsPerFunction(self):
		
		chordsPerFunction = {}
		for targetFunction in self.chordFunctions():
			tally = 0
			for chordTransition in self.rawTransitionalProbabilityTally():
				if chordTransition[0] == targetFunction:
					tally = tally + int(chordTransition[2])
			chordsPerFunction[targetFunction] = tally
		return chordsPerFunction
	
	def chordsPerFunctionSpecial(self, conditionalTally):
		
		chordsPerFunction = {}
		for targetFunction in self.chordFunctions():
			tally = 0
			for chordTransition in conditionalTally:
				if chordTransition[0] == targetFunction:
					tally = tally + int(chordTransition[2])
			chordsPerFunction[targetFunction] = tally
		return chordsPerFunction
	
	def transitionCount(self, targetFunction, followingFunction):
	
		tally = 0
		for chord in self.expandChords():
			if chord[1] == targetFunction:
				if chord[2] == followingFunction:
					tally = tally + 1
		return tally

	def transitionCountNoPhraseBreaks(self, targetFunction, followingFunction):
	
		tally = 0
		for chord in self.expandChords():
			if chord[1] == targetFunction:
				if chord[2] == followingFunction:
					if chord[3] == '0':
						tally = tally + 1
		return tally	

	def transitionCountNoModuleBreaks(self, targetFunction, followingFunction):
	
		tally = 0
		for chord in self.expandChords():
			if chord[1] == targetFunction:
				if chord[2] == followingFunction:
					if chord[4] == '0':
						tally = tally + 1
		return tally	

	def transitionCountWithinModuleNoPhraseBreaks(self, module, targetFunction, followingFunction):
	
		tally = 0
		for chord in self.expandChords():
			if chord[0] == module:
				if chord[1] == targetFunction:
					if chord[2] == followingFunction:
						if chord[3] == '0':
							if chord[4] == '0':
								tally = tally + 1
		return tally

	def transitionCountWithinModule(self, module, targetFunction, followingFunction):
	
		tally = 0
		for chord in self.expandChords():
			if chord[0] == module:
				if chord[1] == targetFunction:
					if chord[2] == followingFunction:
						if chord[4] == '0':
							tally = tally + 1
		return tally

	def rawTransitionalProbabilityTally(self):
	
		tallyAnalysis = []
		for chordFunction in self.chordFunctions():
			for followingFunction in self.chordFunctions():
				tallyAnalysis.append([chordFunction, followingFunction, self.transitionCount(chordFunction, followingFunction)])
				
		return tallyAnalysis

	def rawTransitionalProbabilityTallyCorpusReferenced(self, corpus):
	
		tallyAnalysis = {}
		for chordTransition in self.rawTransitionalProbabilityTally():
			target = chordTransition[0]
			followingChord = chordTransition[1]
			transition = target + '-' + followingChord
			tallyAnalysis[transition] = int(chordTransition[2])

		convertedAnalysis = {}
		for transition in corpus.chordTransitions():
			if transition in tallyAnalysis:
				convertedAnalysis[transition] = tallyAnalysis[transition]
			else:
				convertedAnalysis[transition] = int(0)
		return convertedAnalysis

	def rawTransitionalProbability(self):
	
		probabilityAnalysis = {}
		for chordTransition in self.rawTransitionalProbabilityTally():
			target = chordTransition[0]
			followingChord = chordTransition[1]
			transition = target + '-' + followingChord
			tally = float(chordTransition[2])
			totalPerFunction = float(self.chordsPerFunction()[target])
			if totalPerFunction == 0:
				probability = 0
			else:
				probability = float(tally / totalPerFunction)
			probabilityAnalysis[transition] = probability
		return probabilityAnalysis
	
	def rawTransitionalProbabilityCorpusReferenced(self, corpus):
	
		probabilityAnalysis = {}
		for chordTransition in self.rawTransitionalProbabilityTally():
			target = chordTransition[0]
			followingChord = chordTransition[1]
			transition = target + '-' + followingChord
			tally = float(chordTransition[2])
			totalPerFunction = float(self.chordsPerFunction()[target])
			if totalPerFunction == 0:
				probability = 0
			else:
				probability = float(tally / totalPerFunction)
			probabilityAnalysis[transition] = probability

		convertedAnalysis = {}
		for transition in corpus.chordTransitions():
			if transition in probabilityAnalysis:
				convertedAnalysis[transition] = probabilityAnalysis[transition]
			else:
				convertedAnalysis[transition] = float(0)
		return convertedAnalysis
	
	def transitionalProbabilityNoModuleBreaksTally(self):
	
		tallyAnalysis = []
		for chordFunction in self.chordFunctions():
			for followingFunction in self.chordFunctions():
				tallyAnalysis.append([chordFunction, followingFunction, self.transitionCountNoModuleBreaks(chordFunction, followingFunction)])
				
		return tallyAnalysis

	def transitionalProbabilityNoModuleBreaks(self):
	
		probabilityAnalysis = {}
		for chordTransition in self.transitionalProbabilityNoModuleBreaksTally():
			target = chordTransition[0]
			followingChord = chordTransition[1]
			transition = target + '-' + followingChord
			tally = float(chordTransition[2])
			totalPerFunction = float(self.chordsPerFunctionSpecial(self.transitionalProbabilityNoModuleBreaksTally())[target])
			if totalPerFunction == 0:
				probability = 0
			else:
				probability = float(tally / totalPerFunction)
			probabilityAnalysis[transition] = probability
		return probabilityAnalysis
	
	def transitionalProbabilityNoModuleBreaksCorpusReferenced(self, corpus):
	
		probabilityAnalysis = {}
		for chordTransition in self.transitionalProbabilityNoModuleBreaksTally():
			target = chordTransition[0]
			followingChord = chordTransition[1]
			transition = target + '-' + followingChord
			tally = float(chordTransition[2])
			totalPerFunction = float(self.chordsPerFunctionSpecial(self.transitionalProbabilityNoModuleBreaksTally())[target])
			if totalPerFunction == 0:
				probability = 0
			else:
				probability = float(tally / totalPerFunction)
			probabilityAnalysis[transition] = probability

		convertedAnalysis = {}
		for transition in corpus.chordTransitions():
			if transition in probabilityAnalysis:
				convertedAnalysis[transition] = probabilityAnalysis[transition]
			else:
				convertedAnalysis[transition] = float(0)
		return convertedAnalysis
	
	def transitionalProbabilityNoPhraseBreaksTally(self):
	
		tallyAnalysis = []
		for chordFunction in self.chordFunctions():
			for followingFunction in self.chordFunctions():
				tallyAnalysis.append([chordFunction, followingFunction, self.transitionCountNoPhraseBreaks(chordFunction, followingFunction)])
				
		return tallyAnalysis

	def transitionalProbabilityNoPhraseBreaks(self):
	
		probabilityAnalysis = {}
		for chordTransition in self.transitionalProbabilityNoPhraseBreaksTally():
			target = chordTransition[0]
			followingChord = chordTransition[1]
			transition = target + '-' + followingChord
			tally = float(chordTransition[2])
			totalPerFunction = float(self.chordsPerFunctionSpecial(self.transitionalProbabilityNoPhraseBreaksTally())[target])
			if totalPerFunction == 0:
				probability = 0
			else:
				probability = float(tally / totalPerFunction)
			probabilityAnalysis[transition] = probability
		return probabilityAnalysis

	def transitionalProbabilityNoPhraseBreaksCorpusReferenced(self, corpus):
	
		probabilityAnalysis = {}
		for chordTransition in self.transitionalProbabilityNoPhraseBreaksTally():
			target = chordTransition[0]
			followingChord = chordTransition[1]
			transition = target + '-' + followingChord
			tally = float(chordTransition[2])
			totalPerFunction = float(self.chordsPerFunctionSpecial(self.transitionalProbabilityNoPhraseBreaksTally())[target])
			if totalPerFunction == 0:
				probability = 0
			else:
				probability = float(tally / totalPerFunction)
			probabilityAnalysis[transition] = probability

		convertedAnalysis = {}
		for transition in corpus.chordTransitions():
			if transition in probabilityAnalysis:
				convertedAnalysis[transition] = probabilityAnalysis[transition]
			else:
				convertedAnalysis[transition] = float(0)
		return convertedAnalysis

	def transitionalProbabilityWithinModuleTally(self, module):
	
		tallyAnalysis = []
		for chordFunction in self.chordFunctions():
			for followingFunction in self.chordFunctions():
				tallyAnalysis.append([chordFunction, followingFunction, self.transitionCountWithinModule(module, chordFunction, followingFunction)])
				
		return tallyAnalysis

	def transitionalProbabilityWithinModule(self, module):
	
		probabilityAnalysis = {}
		for chordTransition in self.transitionalProbabilityWithinModuleTally(module):
			target = chordTransition[0]
			followingChord = chordTransition[1]
			transition = target + '-' + followingChord
			tally = float(chordTransition[2])
			totalPerFunction = float(self.chordsPerFunctionSpecial(self.transitionalProbabilityWithinModuleTally(module))[target])
			if totalPerFunction == 0:
				probability = 0
			else:
				probability = float(tally / totalPerFunction)
			probabilityAnalysis[transition] = probability
		return probabilityAnalysis
	
	def transitionalProbabilityWithinModuleCorpusReferenced(self, module, corpus):
	
		probabilityAnalysis = {}
		for chordTransition in self.transitionalProbabilityWithinModuleTally(module):
			target = chordTransition[0]
			followingChord = chordTransition[1]
			transition = target + '-' + followingChord
			tally = float(chordTransition[2])
			totalPerFunction = float(self.chordsPerFunctionSpecial(self.transitionalProbabilityWithinModuleTally(module))[target])
			if totalPerFunction == 0:
				probability = 0
			else:
				probability = float(tally / totalPerFunction)
			probabilityAnalysis[transition] = probability

		convertedAnalysis = {}
		for transition in corpus.chordTransitions():
			if transition in probabilityAnalysis:
				convertedAnalysis[transition] = probabilityAnalysis[transition]
			else:
				convertedAnalysis[transition] = float(0)
		return convertedAnalysis
	
	def transitionalProbabilityWithinModuleNoPhraseBreaksTally(self, module):
	
		tallyAnalysis = []
		for chordFunction in self.chordFunctions():
			for followingFunction in self.chordFunctions():
				tallyAnalysis.append([chordFunction, followingFunction, self.transitionCountWithinModuleNoPhraseBreaks(module, chordFunction, followingFunction)])
				
		return tallyAnalysis

	def transitionalProbabilityWithinModuleNoPhraseBreaks(self, module):
	
		probabilityAnalysis = {}
		for chordTransition in self.transitionalProbabilityWithinModuleNoPhraseBreaksTally(module):
			target = chordTransition[0]
			followingChord = chordTransition[1]
			transition = target + '-' + followingChord
			tally = float(chordTransition[2])
			totalPerFunction = float(self.chordsPerFunctionSpecial(self.transitionalProbabilityWithinModuleNoPhraseBreaksTally(module))[target])
			if totalPerFunction == 0:
				probability = 0
			else:
				probability = float(tally / totalPerFunction)
			probabilityAnalysis[transition] = probability
		return probabilityAnalysis

	def transitionalProbabilityWithinModuleNoPhraseBreaksCorpusReferenced(self, module, corpus):
	
		probabilityAnalysis = {}
		for chordTransition in self.transitionalProbabilityWithinModuleNoPhraseBreaksTally(module):
			target = chordTransition[0]
			followingChord = chordTransition[1]
			transition = target + '-' + followingChord
			tally = float(chordTransition[2])
			totalPerFunction = float(self.chordsPerFunctionSpecial(self.transitionalProbabilityWithinModuleNoPhraseBreaksTally(module))[target])
			if totalPerFunction == 0:
				probability = 0
			else:
				probability = float(tally / totalPerFunction)
			probabilityAnalysis[transition] = probability

		convertedAnalysis = {}
		for transition in corpus.chordTransitions():
			if transition in probabilityAnalysis:
				convertedAnalysis[transition] = probabilityAnalysis[transition]
			else:
				convertedAnalysis[transition] = float(0)
		return convertedAnalysis

	

class CorpusAnalysis():

	def __init__(self):
		self.data = []
		self.repertoire = []
	
	def modules(self):
		
		corpusModules = []
		for song in self.repertoire:
			moduleList = SongAnalysis(song).modules()
			for module in moduleList:
				corpusModules.append(module)
		return sorted(set(corpusModules))

	def chordFunctions(self):
		
		corpusChordFunctions = []
		for song in self.repertoire:
			chordFunctionList = SongAnalysis(song).chordFunctions()
			for function in chordFunctionList:
				corpusChordFunctions.append(function)
		return sorted(set(corpusChordFunctions))

	def chordTransitions(self):
	
		transitions = []
		for targetFunction in self.chordFunctions():
			for followingFunction in self.chordFunctions():
				transition = targetFunction + '-' + followingFunction
				transitions.append(transition)
		return transitions
		
	def transitionalTally(self):
	
		resultsTable = []
		header = []
		tallyResults = {}
		for song in self.repertoire:
			tallyResults[song] = SongAnalysis(song).rawTransitionalProbabilityTallyCorpusReferenced(self)
		header.append('Song')
		for transition in self.chordTransitions():
			header.append(transition)
		resultsTable.append(header)
		for song in self.repertoire:
			dataList = []
			dataList.append(song)
			for transition in self.chordTransitions():
				dataList.append(tallyResults[song][transition])
			resultsTable.append(dataList)
		return resultsTable

	def transitionalProbability(self):
	
		resultsTable = []
		header = []
		probabilityResults = {}
		for song in self.repertoire:
			probabilityResults[song] = SongAnalysis(song).rawTransitionalProbabilityCorpusReferenced(self)
		header.append('Song')
		for transition in self.chordTransitions():
			header.append(transition)
		resultsTable.append(header)
		for song in self.repertoire:
			dataList = []
			dataList.append(song)
			for transition in self.chordTransitions():
				dataList.append(probabilityResults[song][transition])
			resultsTable.append(dataList)
		return resultsTable

	def transitionalProbabilityNoModuleBreaks(self):
	
		resultsTable = []
		header = []
		probabilityResults = {}
		for song in self.repertoire:
			probabilityResults[song] = SongAnalysis(song).transitionalProbabilityNoModuleBreaksCorpusReferenced(self)
		header.append('Song')
		for transition in self.chordTransitions():
			header.append(transition)
		resultsTable.append(header)
		for song in self.repertoire:
			dataList = []
			dataList.append(song)
			for transition in self.chordTransitions():
				dataList.append(probabilityResults[song][transition])
			resultsTable.append(dataList)
		return resultsTable

	def transitionalProbabilityNoPhraseBreaks(self):
	
		resultsTable = []
		header = []
		probabilityResults = {}
		for song in self.repertoire:
			probabilityResults[song] = SongAnalysis(song).transitionalProbabilityNoPhraseBreaksCorpusReferenced(self)
		header.append('Song')
		for transition in self.chordTransitions():
			header.append(transition)
		resultsTable.append(header)
		for song in self.repertoire:
			dataList = []
			dataList.append(song)
			for transition in self.chordTransitions():
				dataList.append(probabilityResults[song][transition])
			resultsTable.append(dataList)
		return resultsTable

	def transitionalProbabilityWithinModule(self, module):
	
		resultsTable = []
		header = []
		probabilityResults = {}
		for song in self.repertoire:
			probabilityResults[song] = SongAnalysis(song).transitionalProbabilityWithinModuleCorpusReferenced(module, self)
		header.append('Song')
		for transition in self.chordTransitions():
			header.append(transition)
		resultsTable.append(header)
		for song in self.repertoire:
			dataList = []
			dataList.append(song)
			for transition in self.chordTransitions():
				dataList.append(probabilityResults[song][transition])
			resultsTable.append(dataList)
		return resultsTable

	def transitionalProbabilityWithinModuleNoPhraseBreaks(self, module):
	
		resultsTable = []
		header = []
		probabilityResults = {}
		for song in self.repertoire:
			probabilityResults[song] = SongAnalysis(song).transitionalProbabilityWithinModuleNoPhraseBreaksCorpusReferenced(module, self)
		header.append('Song')
		for transition in self.chordTransitions():
			header.append(transition)
		resultsTable.append(header)
		for song in self.repertoire:
			dataList = []
			dataList.append(song)
			for transition in self.chordTransitions():
				dataList.append(probabilityResults[song][transition])
			resultsTable.append(dataList)
		return resultsTable
		
def convertToCorpusReferenced(songAnalysis, corpus):

	convertedAnalysis = {}
	for transition in corpus.chordTransitions():
		if transition in songAnalysis:
			convertedAnalysis[transition] = songAnalysis[transition]
		else:
			convertedAnalysis[transition] = float(0)
	return convertedAnalysis