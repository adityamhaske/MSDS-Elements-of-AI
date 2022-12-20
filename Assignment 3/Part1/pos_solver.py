from math import log,exp
from numpy import random as m
from collections import defaultdict

DEBUG = []
BlankSpace,CountOfOne,CountOfTwo,WorstCaseProb,TagPeriod= " ",1,2,10**(-10),"."
class Solver:
    def __init__(self):
        self.CountAllWords,self.CountOfAllLines,self.SimplePostValue,self.HMMPostValue = 0,0,0,0
        self.SpeechTagsC,self.SpeechTagProb,self.StateChangeC,self.StateChangeProb,self.MCMCStateChangeC,self.MCMCStateChangeProb,self.ViMCMCdic = dict(),dict(),dict(),dict(),dict(),dict(),defaultdict(int)
        self.ObservedChangeC,self.ObservedChangeProb,self.HashOfWords,self.HashOfTags = dict(), dict(),defaultdict(bool),defaultdict(bool)       
        
    # We are using the logarithmic apporach for posterior calculation to avoid dealing with extreemly small values of probability
    #caused due to the repeated multiplication of fractional probablities
    def posterior(self, model, sentence, label):
        #Initializing the the used variables with 0 and storing the number of words in the sentence for calculation
        CalculatedPost,wordcount = 0,len(sentence)
        if model == "Simple":
            #Calculating the simple probability for the words in from the emission probabilities
            for AccessIndex in range(wordcount):
                if self.ObservedChangeProb.get(sentence[AccessIndex]) and self.ObservedChangeProb[sentence[AccessIndex]].get(label[AccessIndex]):CalculatedPost = CalculatedPost+log(self.ObservedChangeProb[sentence[AccessIndex]][label[AccessIndex]])
                CalculatedPost =CalculatedPost+log(self.SpeechTagProb[label[AccessIndex]])
            return CalculatedPost
        
        #Calculating the Complex Probabailities using the 
        elif model == "Complex":return self.Calculate_Chances(sentence, label)
        
        #Calculating the HMM Probabilities
        elif model == "HMM":
            for AccessIndex in range(wordcount):
                if self.ObservedChangeProb.get(sentence[AccessIndex]) and self.ObservedChangeProb[sentence[AccessIndex]].get(label[AccessIndex]):CalculatedPost += log(self.ObservedChangeProb[sentence[AccessIndex]][label[AccessIndex]])
                if not AccessIndex:    CalculatedPost = CalculatedPost + log(self.StateChangeProb[label[AccessIndex]][BlankSpace])
                else:   CalculatedPost = CalculatedPost + log(self.StateChangeProb[label[AccessIndex]][label[AccessIndex-CountOfOne]])
            return CalculatedPost
        else:print("Unknown algo!")

    def train(self, data):
        #print("Training Starts")
        
        #Calculating and storing the total number of sentences present in the training data 
        self.CountOfAllLines =  len(data)
        while data:
            
            #Unpacking the imput dataset into a Tuple/list of words and their corresponding POS Tag 
            ListOfWords,ListOfTags = data.pop()
            
            CurWordCount = len(ListOfTags)
            #print('-.-.-.-.-.-.-.-.-.',CurWordCount)
            
            #Maintaining the count of the number of words processed during each sentence to use during probablility calculations
            self.CountAllWords += CurWordCount
            
            #Iterating through the sentence and indexing for each word and POS Tag individually for storing variaous features
            for AccessIndex in range(CurWordCount):
                
                #Parsing the Words and tag into usable variables for better readability
                CurrWord,CurrPOSTag = ListOfWords[AccessIndex],ListOfTags[AccessIndex]
                
                #Using Default Dictionary to skip checking for a key presence and directly add the words and tags as Hashed dictionary
                self.HashOfWords[CurrWord],self.HashOfTags[CurrPOSTag] = True,True
                
                #Checking if we have a new word to calculate its emission if we dont have a new word we enter to check its POS Tag
                if self.ObservedChangeC.get(CurrWord):
                    #If its not a new word we check if it has been used with the obtain POS Tag curreCly held by it and increment it by 1 or set it as the first use instance
                    if self.ObservedChangeC[CurrWord].get(CurrPOSTag):   self.ObservedChangeC[CurrWord][CurrPOSTag] += CountOfOne
                    #Else initialize the count as 1
                    else:   self.ObservedChangeC[CurrWord][CurrPOSTag] = CountOfOne
                else:
                    #If it is a new word we create the new emission record for the word and the usage as the current POS Tag
                    self.ObservedChangeC[CurrWord],self.ObservedChangeC[CurrWord][CurrPOSTag] = dict(),CountOfOne
                    
                #Creating the Observed Emission count for the change in POS labels for the current     
                if self.SpeechTagsC.get(CurrPOSTag):   self.SpeechTagsC[CurrPOSTag] += CountOfOne
                #Else initialize the count as 1
                else:   self.SpeechTagsC[CurrPOSTag] = CountOfOne
                    
                #Specific checking for the first word in the sentence
                if not AccessIndex:
                    #Checking if the Tag is a new tag and increase the count respectively
                    if self.StateChangeC.get(CurrPOSTag):
                        #Adding Blank space transition count or incrementing it by 1
                        if self.StateChangeC[CurrPOSTag].get(BlankSpace):     self.StateChangeC[CurrPOSTag][BlankSpace] += CountOfOne
                        #Else initialize the count as 1
                        else:   self.StateChangeC[CurrPOSTag][BlankSpace] = CountOfOne
                    else:
                        #Creating the word transmission count
                        self.StateChangeC[CurrPOSTag] = dict()
                        #Creating the word from blank space transmission count
                        self.StateChangeC[CurrPOSTag][BlankSpace] = CountOfOne

                else:
                    if self.StateChangeC.get(CurrPOSTag):
                        if self.StateChangeC[CurrPOSTag].get(ListOfTags[AccessIndex-CountOfOne]):   self.StateChangeC[CurrPOSTag][ListOfTags[AccessIndex-CountOfOne]] += CountOfOne
                        #Else initialize the count as 1
                        else:   self.StateChangeC[CurrPOSTag][ListOfTags[AccessIndex-CountOfOne]] = CountOfOne
                    else:
                        #Creating the word transmission count
                        self.StateChangeC[CurrPOSTag] = dict()
                        #Creating the word from previous transmission count
                        self.StateChangeC[CurrPOSTag][ListOfTags[AccessIndex-CountOfOne]] = CountOfOne
        
                        
                #Creating the MCMC Transition counts after atleats 2 words are input to get previous 2 word values
                if AccessIndex>=CountOfTwo:
                    if self.MCMCStateChangeC.get(CurrPOSTag):
                        #Checking if the immmediate previous variable is present to calculate the transmission probability and move to the 2nd previous word
                        if self.MCMCStateChangeC[CurrPOSTag].get(ListOfTags[AccessIndex-CountOfOne]):
                            #Checking if the second previous variable is present to calculate the transmission probability and increment the count by a count of 1
                            if  self.MCMCStateChangeC[CurrPOSTag][ListOfTags[AccessIndex-CountOfOne]].get(ListOfTags[AccessIndex-CountOfTwo]):   self.MCMCStateChangeC[CurrPOSTag][ListOfTags[AccessIndex-CountOfOne]][ListOfTags[AccessIndex-CountOfTwo]] += CountOfOne
                            #initialize the count as 1
                            else:self.MCMCStateChangeC[CurrPOSTag][ListOfTags[AccessIndex-CountOfOne]][ListOfTags[AccessIndex-CountOfTwo]] = CountOfOne
                        else:
                            #Creating the word to last word transmission count
                            self.MCMCStateChangeC[CurrPOSTag][ListOfTags[AccessIndex-CountOfOne]] = dict()
                            #Creating the word to last word to second last word transmission count
                            self.MCMCStateChangeC[CurrPOSTag][ListOfTags[AccessIndex-CountOfOne]][ListOfTags[AccessIndex-CountOfTwo]] = CountOfOne
                    else:
                        #else we create dual nested transmission count for the MCMC network
                        #first dict for the target word
                        self.MCMCStateChangeC[CurrPOSTag] = dict()
                        #second dict for the first previous word 
                        self.MCMCStateChangeC[CurrPOSTag][ListOfTags[AccessIndex-CountOfOne]] = dict()
                        #third dict for the second previous word
                        self.MCMCStateChangeC[CurrPOSTag][ListOfTags[AccessIndex-CountOfOne]][ListOfTags[AccessIndex-CountOfTwo]] = CountOfOne
        if 1 in DEBUG:
            print('-------------------------',self.SpeechTagsC,'-------------------------')
            print('-----------------------------------------------------------------------------------------------------------')
        if 2 in DEBUG:
            print('-------------------------',self.StateChangeC,'-------------------------')
            print('-----------------------------------------------------------------------------------------------------------')
        if 3 in DEBUG:
            print('-------------------------',self.MCMCStateChangeC,'-------------------------')
            print('-----------------------------------------------------------------------------------------------------------')
        if 4 in DEBUG:   
            print('-------------------------',self.ObservableChangeC,'-------------------------')
            print('-----------------------------------------------------------------------------------------------------------')
        
        #Rewrite the Debug Variable at the top of the line to print Necessary variables
        if 5 in DEBUG:   
            print('-------------------------',self.CountAllWords,self.CountOfAllLines,'-------------------------')
            print('-----------------------------------------------------------------------------------------------------------')
        if 6 in DEBUG:   
            print('-------------------------',self.HashOfWords,'-------------------------')
            print('-----------------------------------------------------------------------------------------------------------')
        if 7 in DEBUG:   
            print('-------------------------',self.HashOfTags,'-------------------------')
            print('-----------------------------------------------------------------------------------------------------------')
        
    
        for instance in self.HashOfWords:
            #Evaluating the emission probabilities from the HashOfWords using previously calculated observed emission counts
            for SpeechTag in self.HashOfTags:
                if self.ObservedChangeProb.get(instance) == None:   self.ObservedChangeProb[instance] = dict()
                if self.ObservedChangeC[instance].get(SpeechTag):   self.ObservedChangeProb[instance][SpeechTag] = float(self.ObservedChangeC[instance][SpeechTag]) / self.SpeechTagsC[SpeechTag]
                else:   self.ObservedChangeProb[instance][SpeechTag] = WorstCaseProb
                
        if 8 in DEBUG:   
            print('-------------------------',self.ObservedChangeProb,'-------------------------')
            print('-----------------------------------------------------------------------------------------------------------')

        for SpeechTag in self.HashOfTags:
            #Evaluating the Transition probabilities from the HashOfTags using previously calculated state change transition counts
            if self.StateChangeProb.get(SpeechTag)==None: self.StateChangeProb[SpeechTag] = dict()
            for SimpleSpeechTagOneWordBack in self.HashOfTags:
                if self.StateChangeC[SpeechTag].get(SimpleSpeechTagOneWordBack):    self.StateChangeProb[SpeechTag][SimpleSpeechTagOneWordBack] = float(self.StateChangeC[SpeechTag][SimpleSpeechTagOneWordBack]) / (self.CountAllWords-self.CountOfAllLines)
                else:   self.StateChangeProb[SpeechTag][SimpleSpeechTagOneWordBack] = WorstCaseProb
        if 9 in DEBUG:   
            print('-------------------------',self.StateChangeProb,'-------------------------')
            print('-----------------------------------------------------------------------------------------------------------')

        for SpeechTag in self.HashOfTags:
            #Evaluating the MCMC Transition probabilities from the HashOfTags using previously calculated MCMC state change transition counts
            if self.MCMCStateChangeProb.get(SpeechTag)==None:  self.MCMCStateChangeProb[SpeechTag] = dict()
            for SpeechTagOneWordBack in self.HashOfTags:
                if  self.MCMCStateChangeC[SpeechTag].get(SpeechTagOneWordBack):
                    if self.MCMCStateChangeProb[SpeechTag].get(SpeechTagOneWordBack)==None:   self.MCMCStateChangeProb[SpeechTag][SpeechTagOneWordBack] = dict()
                    for SpeechTagTwoWordBack in self.HashOfTags:
                        if self.MCMCStateChangeC[SpeechTag][SpeechTagOneWordBack].get(SpeechTagTwoWordBack):   self.MCMCStateChangeProb[SpeechTag][SpeechTagOneWordBack][SpeechTagTwoWordBack] = float(self.MCMCStateChangeC[SpeechTag][SpeechTagOneWordBack][SpeechTagTwoWordBack]) / (self.CountAllWords-(CountOfTwo*self.CountOfAllLines))
                        else:self.MCMCStateChangeProb[SpeechTag][SpeechTagOneWordBack][SpeechTagTwoWordBack] = WorstCaseProb
                else:
                    if self.MCMCStateChangeProb[SpeechTag].get(SpeechTagOneWordBack)==None:   self.MCMCStateChangeProb[SpeechTag][SpeechTagOneWordBack] = dict()
                    for SpeechTagTwoWordBack in self.HashOfTags:   self.MCMCStateChangeProb[SpeechTag][SpeechTagOneWordBack][SpeechTagTwoWordBack] = WorstCaseProb
        if 10 in DEBUG:   
            print('-------------------------',self.MCMCStateChangeProb,'-------------------------')
            print('-----------------------------------------------------------------------------------------------------------')

        for SpeechTag in self.HashOfTags:
            if self.StateChangeC[SpeechTag].get(BlankSpace):self.StateChangeProb[SpeechTag][BlankSpace] = float(self.StateChangeC[SpeechTag][BlankSpace]/self.CountOfAllLines)
            else:self.StateChangeProb[SpeechTag][BlankSpace] = WorstCaseProb
            
        if 11 in DEBUG:   
            print('-------------------------',self.StateChangeProb,'-------------------------')
            print('-----------------------------------------------------------------------------------------------------------')
            
        for SpeechTag in self.HashOfTags:self.SpeechTagProb[SpeechTag] = self.SpeechTagsC[SpeechTag] / self.CountAllWords
        
        if 12 in DEBUG:   
            print('-------------------------',self.SpeechTagProb,'-------------------------')
            print('-----------------------------------------------------------------------------------------------------------')
        print("Training Ends")
        
    def simplified(self, sentence):
        #Initilaizing the POS tag storage list to store the predicted POS based on the presence of the word and its training probablilities
        Maybe_SpeechTag = list()
        for index1,instance in enumerate(sentence):
            #For each word instance from the sentence we calculate the posterior probability foor the words 
            CurrProb,CurTag = -0.5,TagPeriod
            for index2,SpeechTag in enumerate(self.HashOfTags):
                #Checking if the word being tested is new to avoid assigning to 0
                if self.ObservedChangeProb.get(instance) == None: Min_Posterior = WorstCaseProb
                #else we calculate the posterior value and use it to find the likelihood for the Speech tag
                else:   Min_Posterior = self.ObservedChangeProb[instance][SpeechTag]
                #Expected Speech tag ebing calculated and store it iin a list
                if self.SpeechTagProb[SpeechTag]*Min_Posterior > CurrProb:  CurrProb,CurTag = self.SpeechTagProb[SpeechTag]*Min_Posterior,SpeechTag
                #print(f"current word  = {instance} and current predicted tag = {CurTag}" )
            Maybe_SpeechTag=Maybe_SpeechTag+[CurTag]
        if 13 in DEBUG: print(f"Speech tagged sentence for simplified  = {Maybe_SpeechTag}")
        return Maybe_SpeechTag

    def complex_mcmc(self, sentence):
        #Result list initialization and Obtainining the viterbi prob for the sentence
        PlausibleTag,RandomizedInstances = self.hmm_viterbi(sentence),list()
        #Sampling Iterations for gibbs sampling
        for _ in range(0,180):
            #Randomized Sampling for the Plausibility of speech tag
            Plausibility = self.Sampler_gb(sentence, PlausibleTag)
            #Burning iterations for the intances
            if(_>90):RandomizedInstances=RandomizedInstances+[Plausibility]
            _=_+CountOfOne
        #Unpacking the instances after sampling and burnin
        UnpackedIntances = list(zip(*RandomizedInstances))
        Artifice = [max(set(PackedElement), key=PackedElement.count) for PackedElement in UnpackedIntances]
        if 13 in DEBUG: print(f"Speech tagged sentence for MCMC  = {UnpackedIntances}")
        #Calculating the count of each unpacked element in the unpacker plausibility list
        PlausibleTag = Artifice.copy()
        return PlausibleTag

    def Sampler_gb(self, sentence, PlausibleTag):
        #Initializing the Word Count and The sampled speech tags
        wordcount,ChosenSpeechTag,FirstElem = len(sentence),list(PlausibleTag),0
        #Iterating individually on the words of the sentence
        self.ViMCMCdic[wordcount] = ChosenSpeechTag
        for AccessIndex,Instance in enumerate(sentence):
            #Initializing the Prediciton tag and probability
            SpeechTag,SpeechTagProb = list(),list()
            #Iteratinf for each Unique POS present in the Hashtags
            for ind,ActiveSpeechTag in enumerate(self.HashOfTags):
                #Assign the Tags
                SpeechTag,ChosenSpeechTag[AccessIndex] = SpeechTag+[ActiveSpeechTag],ActiveSpeechTag
                TotalRuns = AccessIndex+ind
                self.ViMCMCdic[TotalRuns] = SpeechTag
                #Calculating the prob of getting the tag for the sentence
                curr_SpeechTagProb = self.Calculate_Chances(sentence, ChosenSpeechTag)
                SpeechTagProb+=[exp(curr_SpeechTagProb)]
            if 14 in DEBUG: print(f"Speech tagged gibbs  = {SpeechTagProb}")
            CombinedProb = sum(SpeechTagProb)
            if not CombinedProb:ChosenSpeechTag[AccessIndex] = SpeechTag[FirstElem]
            else:
                PartialProb = list()
                for chance in SpeechTagProb:PartialProb.append(chance/CombinedProb)
                ChosenSpeechTag[AccessIndex] = m.choice(SpeechTag, p=PartialProb)
        if 15 in DEBUG: print(f"final gibbs tags= {ChosenSpeechTag}")
        return ChosenSpeechTag

    def Calculate_Chances(self, line, PlausibleTag):
        #Initializing the chances of getting the tag and wordcount
        wordcount,chances = len(line),0
        for WordIndex,Word in enumerate(line):
            #Enumerating the words and corresponding tags for the processing of chances of tha tag being true for the words
            SpeechTag = PlausibleTag[WordIndex]
            #Min prob to avoid 0 output
            if self.ObservedChangeProb.get(Word) == None:RunningProb = WorstCaseProb
            #Assigning the Emission probability and summing up for the chance of true probability
            else:RunningProb = self.ObservedChangeProb[Word][SpeechTag]
            chances=chances+log(RunningProb)
            self.ViMCMCdic[wordcount] = chances
            # Taking log of the Tag probabilities for summing for first word
            if not WordIndex:chances += log(self.SpeechTagProb[SpeechTag])
            #MCMC type probability calculation of previous word 
            elif WordIndex==CountOfOne:
                SpeechTagOneWordBack = PlausibleTag[WordIndex-CountOfOne]
                chances += log(self.StateChangeProb[SpeechTag][SpeechTagOneWordBack])
            #MCMC type probability calculation of second previous and further words
            else:
                SpeechTagOneWordBack,SpeechTagTwoWordBack = PlausibleTag[WordIndex-CountOfOne],PlausibleTag[WordIndex-CountOfTwo]
                chances=chances+log(self.MCMCStateChangeProb[SpeechTag][SpeechTagOneWordBack][SpeechTagTwoWordBack])
        if 16 in DEBUG: print(f"Probabilities of the tags= {chances}")
        return chances


    def hmm_viterbi(self, sentence):
        #Setting the default probability for the initial guess of word speech tag
        PlausibleTag,SpeechTagindexStoring,viterbi_Dynamic,FirstElem,wordcount = ["adp" for AccessIndex,_ in enumerate(sentence)],dict(),[[(0, TagPeriod, TagPeriod)]*12 for _,__ in enumerate(sentence)],0,len(sentence)
        l = wordcount-CountOfOne
        #Storing tag and index pairs
        for SpeechTagindex,SpeechTag in enumerate(self.HashOfTags):SpeechTagindexStoring[SpeechTag] = SpeechTagindex
        #Storing tag and index pairs
        for SpeechTagindex,SpeechTag in enumerate(self.HashOfTags):
            if self.ObservedChangeProb.get(sentence[FirstElem]) == None:RunningProb = WorstCaseProb
            else:RunningProb = self.ObservedChangeProb[sentence[FirstElem]][SpeechTag]
            #Word-Blank space transition probability with corresponding tags
            viterbi_Dynamic[FirstElem][SpeechTagindex]=(self.StateChangeProb[SpeechTag][BlankSpace]*RunningProb,SpeechTag,SpeechTag)
        if 17 in DEBUG: print(f"Dynamic prog viterbi 2d array set of the tags= {viterbi_Dynamic}")
        for AccessIndex in range(CountOfOne, wordcount):
            #Calculating the One word back and two word back tag probabilities
            for SpeechTagIndex1,SpeechTag in enumerate(self.HashOfTags):
                #Init Values
                SimpleSpeechTagOneWordBack,CurrProb,TagVal = TagPeriod,-0.5,"noun"
                #Second word probablilities
                for SpeechTagIndex2,pos1 in enumerate(self.HashOfTags):
                    #Emission probability Used to update the viterby array
                    if viterbi_Dynamic[AccessIndex-CountOfOne][SpeechTagIndex2][FirstElem]*self.StateChangeProb[SpeechTag][viterbi_Dynamic[AccessIndex-CountOfOne][SpeechTagIndex2][CountOfOne]] > CurrProb:
                        CurrProb = viterbi_Dynamic[AccessIndex-CountOfOne][SpeechTagIndex2][FirstElem]*self.StateChangeProb[SpeechTag][viterbi_Dynamic[AccessIndex-CountOfOne][SpeechTagIndex2][CountOfOne]]
                        SimpleSpeechTagOneWordBack = viterbi_Dynamic[AccessIndex-CountOfOne][SpeechTagIndex2][CountOfOne]
                        self.ViMCMCdic[TagVal] = CurrProb
                #Emission probability Used to update the viterby array
                if self.ObservedChangeProb.get(sentence[AccessIndex])==None:RunningProb = WorstCaseProb
                else:RunningProb = self.ObservedChangeProb[sentence[AccessIndex]][SpeechTag]
                viterbi_Dynamic[AccessIndex][SpeechTagIndex1] = (CurrProb*RunningProb,SpeechTag,SimpleSpeechTagOneWordBack)
        if 18 in DEBUG: print(f"Plausible array of the viterby probs= {viterbi_Dynamic}")
        ExpectedSpeechTag,CurrProb = TagPeriod,-0.5
        for SpeechTagIndex,SpeechTag in enumerate(self.HashOfTags):
            if viterbi_Dynamic[wordcount-CountOfOne][SpeechTagIndex][FirstElem]>CurrProb:
                CurrProb = viterbi_Dynamic[wordcount-CountOfOne][SpeechTagIndex][FirstElem]
                ExpectedSpeechTag = viterbi_Dynamic[wordcount-CountOfOne][SpeechTagIndex][CountOfOne]
        if CurrProb:self.HMMPostValue=log(CurrProb)
        #Last part to calculate the final plausible tags for the passed sentence by referring the Viterby DP array
        for _,__ in enumerate(sentence):
            PlausibleTag[l] = ExpectedSpeechTag
            ExpectedSpeechTag = viterbi_Dynamic[l][SpeechTagindexStoring[ExpectedSpeechTag]][CountOfTwo]
            l -=CountOfOne
            
        if 19 in DEBUG: print(f"Deduced set of the tag= {ExpectedSpeechTag}")
        return PlausibleTag

    def solve(self, model, sentence):
        if model == "Simple":
            return self.simplified(sentence)
        elif model == "Complex":
            return self.complex_mcmc(sentence)
        elif model == "HMM":
            return self.hmm_viterbi(sentence)
        else:
            print("Unknown algo!")