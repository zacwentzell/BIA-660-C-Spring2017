"""
Week 2
The script defines a function run(). The function accepts as input the path to a text file and 2 words. It then returns the number of times that each 
word appears in the file.
"""

#define a new function
def run(path,word1,word2):

	freq={} # new dictionary. Maps each word to each frequency 
	
	#initialize the frequency of the two words to zero.
	freq[word1]=0
	freq[word2]=0

	fin=open(path) # open a connection to the file 
	for line in fin: # read the file line by line 
		# lower() converts all the letters in the string to lower-case
		# strip() removes blank space from the start and end of the string
		# split(c) splits the string on the character c and returns a list of the pieces. For example, "A1B1C1D".split('1')" returns [A,B,C,D] 
		words=line.lower().strip().split(' ') 

		# use for to go over all the words in the list 
		for word in words: # for each word in the line
			if word==word1: 
				freq[word1]=freq[word1]+1 # if the word is word1, then increase the count of word1 by 1
			elif word==word2: 
				freq[word2]=freq[word2]+1 # if the word is word2, then increase the count of word2 by 1

	fin.close() #close the connection to the text file 

	return freq[word1],freq[word2]


# use the function 
print run('textfile','blue','yellow')
print run('textfile','the','house')

"""

EXPLANATION
==================

In the beginning, we have freq['blue']=0 and freq['yellow']=0

The first line of the file is:
My name is John and I live in the blue house

After we lower, strip, and split we get the following list of words:
words=['my','name','is','john','and','i','live','in','the','blue','house']

after going over all the words in the list, the counts become:

freq['blue']=1
freq['yellow']=1

We proceed in the same way for all the lines in the file.


NOTES
================
- Remember to use indentation. Best to use a <TAB>. Add one level for each if,for,while

- We create a new dictionary by typing: myDict={}. A dictionary maps keys to values. In our case, words to numbers (their frequencies).
Keys are unique, values are not. Searching for keys in dictionaries is fast!

- Remember to wrap string in quotes ('textfile, 'blue', etc)

"""
