# basrini-rdhonuks-admhaske-a3
## **Part 1**
- Reference for Gibbs and MCMC: 
    - https://www.youtube.com/watch?v=MNHIbOqH3sk&list=PLvcbYUQ5t0UEkf2NUEo7XSsyVTyeEk3Gq&index=9
    - https://en.wikipedia.org/wiki/Gibbs_sampling
### _Assumptions_:
- The main assumption for most of the implementation models is thaat we need to initialize with a min prob in case the words dont exist.
- Then there are various sub assumptions in terms of each Model:-
    - Simple model assumes that the word depends only on the associated speech tags and the general formula can be reduced as P(sentence(i)| word(i)) which is  eaqual to   sentence(i) * P(word(i)|sentence(i))
    - Hidden Markov Models utilizes the tags from the adjacent  words present to generate the probabilities and utilize them to predict the current speech tags
    - Complex Markov takes it one step further by taking 2 previous words in the sentence and also generalize from the training data using the gibbs sampling.
### _Objective_:
- we'll want to estimate the most-probable tag Si for each word Wi, Si = arg max(Si) P(Si = si|W):
Implement part-of-speech tagging using this simple model.
-  Now , a richer Bayes net that incorporates dependencies between words. Implement Viterbi to find the maximum a posteriori (MAP) labeling for the sentence (s1....sN) = arg max (s1....sN) P(Si = sijW).
-  Consider the Bayes Net which could be a better model because it incorporates richer
dependencies between words. But it's not an HMM, so we can't use Viterbi. Implement Gibbs Sampling
to sample from the posterior distribution of Fig 1c, P(SjW). Then estimate the best labeling for each
word.
### _Approach_:
#### Simple Model
- For the simple mode we just calculate the word counts and the transition probabilities for each word and each tag we calculate the transitions using nested dictionaries
```sh
            for index2,SpeechTag in enumerate(HashOfTags):
                if instance not in self.ObservedChangeProb.get(instance): 
                    Min_Posterior=WorstCaseProb
                else:
                    Min_Posterior=self.ObservedChangeProb[instance][SpeechTag]
                if self.SpeechTagProb[SpeechTag]*Min_Posterior > CurrProb:
                    CurrProb=self.SpeechTagProb[SpeechTag]*Min_Posterior
                    CurTag =SpeechTag
```

#### Viterby Model
- For the Viterby mode we use dynamic programming method to generrate the list of lists consisting of the probabilities for usage after initially generating them all as noun
```sh
        for SpeechTagIndex,SpeechTag in enumerate(HashOfTags):
            if viterbi_Dynamic[wordcount-CountOfOne][SpeechTagIndex][0]>CurrProb:
                CurrProb=viterbi_Dynamic[wordcount-1][SpeechTagIndex][0]
                ExpectedSpeechTag=viterbi_Dynamic[wordcount-1][SpeechTagIndex][1]
        if CurrProb:
            self.HMMPostValue=log(CurrProb)
        for _ in range(wordcount,-1):
            PlausibleTag[last to 0]=ExpectedSpeechTag
            ExpectedSpeechTag=viterbi_Dynamic[last to 0][SpeechTagindexStoring[ExpectedSpeechTag]][CountOfTwo]
```

#### Complex MCMC Model
- For the MCMC we utilize the similar nested dict for getting the probs and since gibbs also is applied the code is too huge to be shown here
```sh
    PlausibleTag,RandomizedInstances=self.hmm_viterbi(sentence),list()
    for _ in range(0,180):
        Plausibility=self.Sampler_gb(sentence,PlausibleTag)
        if(_>90):RandomizedInstances=RandomizedInstances+[Plausibility]
        _=_+CountOfOne
    UnpackedIntances=list(zip(*RandomizedInstances))
    Tags=[max(set(PackedElement),key=PackedElement.count) for PackedElement in UnpackedIntances]
 ```

### _Observation and difficulties_:
- Simple model is very efficient and easy to implement and produces acceptable results too
- Viterby runs the best and has balanced complexity and accuracy
- MCMC is too complex for smaller data set and the debuggund is very difficult dur to randomness
- The most commonly observed Speech tag is noun and verb for the dataset and heavily drives the results.
- We get good accuracies for the Word prediction but the entire sentence prediction is limited at best to 51% as shown below in the results using viterby.
### _Results_

<img width="314" alt="SS" src="https://media.github.iu.edu/user/20772/files/43fe7b58-6991-478e-8aae-5d5786736a84">

## **Part 2**

### _Assumptions_:   

- The image contains sentences and words in English.
- The typeface used in the image is the same fixed-width and size. For example, each letter is contained in a box that is 25 pixels height by 16 pixels wide.
- Another presumption we make is that we only take into account the Latin alphabet's 26 capital, 26 lowercase, 10 numerals, spaces, and 7 punctuation-symbol symbols.
- The image's I/O is handled by the skeleton code, which turns the image into a list of lists that represents a two-by-two grid of black and white dots.  

### _Approach_:   

- We have determined the character-to-character transition probabilities for this problem, exactly like we did for the word-to-word transition probabilities in the prior problem.  

### _Simplified Bayes Net_:   
- In this method, we obtain the character with the highest probability using the emission probability. We then join that character to the remainder of the string and output it.  

### _Viterbi-Hidden Markov Models_:  
- For the dynamic programming approach we are storing the probability values in a 2 column matrix   
- I first tested it as the ratio of the total number of pixels to the number of matched pixels. This was a total failure.  
Next approach was assigning categorical emission probabilities depending on level of correctness    
- Also normalized the probabilities for scaling purpose but only for emission probabilities as transition probabilities have very low value so scaled them up a bit in order to have higher contribution to the prediction than just emission probabilities     
- The final results were were correct enough by using this approach   
