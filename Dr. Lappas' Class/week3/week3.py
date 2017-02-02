"""
Reads a list of reviews and decide if each review is positive or negative,
based on the occurences of positive and negative words.
"""

#function that loads a lexicon of positive words to a set and returns the set
def loadLexicon(fname):
    newLex=set()
    lex_conn=open(fname)
    #add every word in the file to the set
    for line in lex_conn:
        newLex.add(line.strip())# remember to strip to remove the lin-change character
    lex_conn.close()

    return newLex

#function that reads in a file with reviews and decides if each review is positive or negative
#The function returns a list of the input reviews and a list of the respective decisions
def run(path):

	decisions=[] 
	reviews=[]
	#load the positive and negative lexicons
	posLex=loadLexicon('positive-words.txt')
	negLex=loadLexicon('negative-words.txt')

	fin=open(path)
	for line in fin: # for every line in the file (1 review per line)
    		posList=[] #list of positive words in the review
    		negList=[] #list of negative words in the review

		line=line.lower().strip()   
		reviews.append(line)
    
    		words=line.split(' ') # slit on the space to get list of words
    
    		for word in words: #for every word in the review
        		if word in posLex: # if the word is in the positive lexicon
            			posList.append(word) #update the positive list for this review
      		  	if word in negLex: # if the word is in the negative lexicon
            			negList.append(word) #update the negative list for this review
           

   	 	decision=0  # 0 for neutral    
    		if len(posList)>len(negList): # more pos words than neg
        		decision=1 # 1 for positive
	    	elif len(negList)>len(posList):  # more neg than pos
        		decision=-1 # -1 for negative
        
		decisions.append(decision)

	fin.close()
	return reviews, decisions 


if __name__ == "__main__": 

	reviews,decisions=run('textfile')

	for i in range(len(reviews)):
		print reviews[i], decisions[i]
		print





