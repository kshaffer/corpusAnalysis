corpusAnalysis
==============

Python module for form-sensitive transitional probability analysis of harmonic structures in corpora of songs/movements

A sample corpus is available from http://www.github.com/kshaffer/CCLI-2011

# License info #

This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with this program.  If not, see <http://www.gnu.org/licenses/>.

# Usage #

Most classes, methods, and functions are fairly self explanatory from looking at the source code, if you are familiar with Python and object-oriented programming. Even if you aren't, here are some sample code snippets for analyzing songs within the CCLI-2011 corpus that should make it pretty easy.

To import songs into a corpus:

	from corpusAnalysis import *
	CCLI = CorpusAnalysis()
	CCLI.repertoire.append('01HowGreatIsOurGod.csv')
	CCLI.repertoire.append('02MightyToSave.csv')
	CCLI.repertoire.append('03OurGod.csv')
	CCLI.repertoire.append('04BlessedBeYourName.csv')
	CCLI.repertoire.append('05HereIAmToWorship.csv')

and so on...

To generate a transitional probability table for all songs in the corpus and write to CSV file:

	results = CCLI.transitionalProbability()
	f = open('./probTable.csv', 'ab')
	w = csv.writer(f, delimiter=',')
	for row in results:
		w.writerow(row)
	f.close()

That should get you going. More details to be added later. Comments and questions welcome!