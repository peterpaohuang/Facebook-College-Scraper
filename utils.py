import spacy
import pickle
import string
import time
import math
import geograpy3

def initializers():
	f = open('distributions.obj', 'rb')
	uniDist = pickle.load(f)
	backwardBiDist = pickle.load(f)
	forwardBiDist = pickle.load(f)
	trigramDist = pickle.load(f)
	wordCasingLookup = pickle.load(f)
	ent_info = uniDist, backwardBiDist, forwardBiDist, trigramDist, wordCasingLookup
	f.close()
	return ent_info


def getScore(prevToken, possibleToken, nextToken, wordCasingLookup, uniDist, backwardBiDist, forwardBiDist, trigramDist):
    pseudoCount = 5.0
    
    #Get Unigram Score
    nominator = uniDist[possibleToken]+pseudoCount    
    denominator = 0    
    for alternativeToken in wordCasingLookup[possibleToken.lower()]:
        denominator += uniDist[alternativeToken]+pseudoCount
        
    unigramScore = nominator / denominator
        
        
    #Get Backward Score  
    bigramBackwardScore = 1
    if prevToken != None:  
        nominator = backwardBiDist[prevToken+'_'+possibleToken]+pseudoCount
        denominator = 0    
        for alternativeToken in wordCasingLookup[possibleToken.lower()]:
            denominator += backwardBiDist[prevToken+'_'+alternativeToken]+pseudoCount
            
        bigramBackwardScore = nominator / denominator
        
    #Get Forward Score  
    bigramForwardScore = 1
    if nextToken != None:  
        nextToken = nextToken.lower() #Ensure it is lower case
        nominator = forwardBiDist[possibleToken+"_"+nextToken]+pseudoCount
        denominator = 0    
        for alternativeToken in wordCasingLookup[possibleToken.lower()]:
            denominator += forwardBiDist[alternativeToken+"_"+nextToken]+pseudoCount
            
        bigramForwardScore = nominator / denominator
        
        
    #Get Trigram Score  
    trigramScore = 1
    if prevToken != None and nextToken != None:  
        nextToken = nextToken.lower() #Ensure it is lower case
        nominator = trigramDist[prevToken+"_"+possibleToken+"_"+nextToken]+pseudoCount
        denominator = 0    
        for alternativeToken in wordCasingLookup[possibleToken.lower()]:
            denominator += trigramDist[prevToken+"_"+alternativeToken+"_"+nextToken]+pseudoCount
            
        trigramScore = nominator / denominator
        
    result = math.log(unigramScore) + math.log(bigramBackwardScore) + math.log(bigramForwardScore) + math.log(trigramScore)
    #print "Scores: %f %f %f %f = %f" % (unigramScore, bigramBackwardScore, bigramForwardScore, trigramScore, math.exp(result))
  
  
    return result

def getTrueCase(tokens, outOfVocabularyTokenOption, wordCasingLookup, uniDist, backwardBiDist, forwardBiDist, trigramDist):
    """
    Returns the true case for the passed tokens.
    @param tokens: Tokens in a single sentence
    @param outOfVocabulariyTokenOption:
        title: Returns out of vocabulary (OOV) tokens in 'title' format
        lower: Returns OOV tokens in lower case
        as-is: Returns OOV tokens as is
    """
    tokensTrueCase = []
    for tokenIdx in range(len(tokens)):
        token = tokens[tokenIdx]
        if token in string.punctuation or token.isdigit():
            tokensTrueCase.append(token)
        else:
            if token in wordCasingLookup:
                if len(wordCasingLookup[token]) == 1:
                    tokensTrueCase.append(list(wordCasingLookup[token])[0])
                else:
                    prevToken = tokensTrueCase[tokenIdx-1] if tokenIdx > 0  else None
                    nextToken = tokens[tokenIdx+1] if tokenIdx < len(tokens)-1 else None
                    
                    bestToken = None
                    highestScore = float("-inf")
                    
                    for possibleToken in wordCasingLookup[token]:
                        score = getScore(prevToken, possibleToken, nextToken, wordCasingLookup, uniDist, backwardBiDist, forwardBiDist, trigramDist)
                           
                        if score > highestScore:
                            bestToken = possibleToken
                            highestScore = score
                        
                    tokensTrueCase.append(bestToken)
                    
                if tokenIdx == 0:
                    tokensTrueCase[0] = tokensTrueCase[0].title();
                    
            else: #Token out of vocabulary
                if outOfVocabularyTokenOption == 'title':
                    tokensTrueCase.append(token.title())
                elif outOfVocabularyTokenOption == 'lower':
                    tokensTrueCase.append(token.lower())
                else:
                    tokensTrueCase.append(token) 
    
    return tokensTrueCase
def capitalize_ents(text, ent_info):
    uniDist, backwardBiDist, forwardBiDist, trigramDist, wordCasingLookup = ent_info
    tokensCorrect = text.split()
    tokens = [token.lower() for token in tokensCorrect]

    tokensTrueCase = getTrueCase(tokens, 'title', wordCasingLookup, uniDist, backwardBiDist, forwardBiDist, trigramDist)
    

    return ' '.join([x.capitalize() if x == "area" else (x.capitalize() if x == "bay" else x) for x in tokensTrueCase])

def extract_location(text, username):
	places = geograpy3.get_place_context(text=text)

	possible_locations = [x for x in places.countries if x.lower() != ' '.join([x.lower() for x in username.split()])] # removes confusion with names and location


	# check if possible locations is within 3 tokens of key words like "from" 
	confirmed_locations = []
	lower_case_text = [x.lower() for x in text.split()]
	for location in possible_locations:
		try:
			location_index = 0
			for i,word in enumerate(lower_case_text):
				if location.split()[0].lower() in word:
					location_index = i

			location_from_difference = location_index-text.split().index("from")
			if location_from_difference < 7 and location_from_difference > 0:
				confirmed_locations.append(location)
		except Exception as e:
			print(e)
			pass

	# check for state abbreviations 
	detected_states = []
	state_abr = ['al', 'ak', 'as', 'az', 'ar', 'ca', 'co', 'ct', 'de', 'dc', 'fm', 'fl', 'ga', 'gu', 'hi', 'id', 'il', 'in', 'ia', 'ks', 'ky', 'la', 'me', 'mh', 'md', 'ma', 'mi', 'mn', 'ms', 'mo', 'mt', 'ne', 'nv', 'nh', 'nj', 'nm', 'ny', 'nc', 'nd', 'mp', 'oh', 'ok', 'or', 'pw', 'pa', 'pr', 'ri', 'sc', 'sd', 'tn', 'tx', 'ut', 'vt', 'vi', 'va', 'wa', 'wv', 'wi', 'wy']
	unpunct_text = ' '.join(lower_case_text).translate(str.maketrans('', '', string.punctuation)).split()
	for x in list(set(state_abr).intersection(unpunct_text)):
		if x not in [z.lower() for z in confirmed_locations]:
			detected_states.append(x.upper())

	for state in detected_states:
		try:
			state_index = 0
			for i,word in enumerate(lower_case_text):
				if state.lower() in word:
					state_index = i

			state_from_difference = state_index-text.split().index("from")
			if state_from_difference < 7 and state_from_difference > 0:
				confirmed_locations.append(state)
		except Exception as e:
			print(e)
			pass

	if len(confirmed_locations) == 0: # if key word filter removed everything, revert to original possible_locations
		return ["Location was not included"]

	return confirmed_locations

def test(text, username):
	ent_info = initializers()
	capitalized_text = capitalize_ents(text, ent_info)
	print(capitalized_text)
	return extract_location(capitalized_text, username)

