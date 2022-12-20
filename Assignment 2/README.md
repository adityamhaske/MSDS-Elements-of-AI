# basrini-rdhonuks-admhaske-a2

#### Team: Srinivasan, Balajee Devesha (basrini@iu.edu), Dhonukshe Rohit (rdhonuks@iu.edu), Mhaske, Aditya Sanjay(admhaske@iu.edu)

B551- Elements of Artificial Intelligence homework 2 submission repo

## **Question 1:**

### **Initial State:**
- The initial state will be a N x N board (N≥8 and N is even) with the 2nd row consisting of white Pikachus and 3rd row consisting white Pichus. On the N-1 and N-2 rows we observe Black Pikachus and Black Pichus respectively. (Pichus and Pikachus are placed in alternate columns in the given rows).

### **Valid states:**
- All the possible states on the board with any arrangements of Pichu, Pikachus and Raichus are considered valid states.

### **Successor Function:** 
- 3 Main types of succesor function for pichu pikachu and raichu
- short representation given by their directions
Here are 3 Successors 
1. Pichu
```python
def successor_pichu(board,N,vertInd,HorInd):

    board_list = []

    if board[vertInd][HorInd] == 'w':
        w_flag = True
        pichu_movset = [(1,-1,2,-2),(1,1,2,2)]
    elif  board[vertInd][HorInd] == 'b':
        w_flag  = False
        pichu_movset = [(-1,1,-2,2),(-1,-1,-2,-2)]
```

2. Pikachu
```python
def successor_pika(board,N,vertInd,HorInd):

    board_list = []
    if board[vertInd][HorInd] == 'W':
        w_flag = True
        pika_pmovset = [(0,0,0,-1,-2,-3),(0,0,0,1,2,3),(1,2,3,0,0,0)]
    elif  board[vertInd][HorInd] == 'B':
        w_flag = False
        pika_pmovset = [(0,0,0,-1,-2,-3),(0,0,0,1,2,3),(-1,-2,-3,0,0,0)]
```

3. Raichu
```python
def successor_raichu(board,N,vertInd,HorInd):

    board_list = []
    linear_directions = [(+0,-1),(+0,+1),(+1,+0),(-1,+0)]
	diag_directions = [(-1,-1),(+1,+1),(-1,+1),(+1,-1)]
 
    if board[vertInd][HorInd] == '@':
        w_flag = True
        InterState = None
    elif board[vertInd][HorInd] == '$':
        w_flag = True
        InterState = None
 

```

### **Goal State**
- Eliminating all the opposing pieces 

### **Approach**
The below psudeo code was taken from the youtube video : https://www.youtube.com/watch?v=l-hh51ncgDI, used to build our code. - The approach calculates the static board score and then adds piece scores to the board score to generate the final score and minmax the obtained score. - The points are inverted for black. - Aggression can be tuned by adding weightage to the '.' chars. We continue to generate outputs until the mothercode exits.


        function minimax(position, depth, alpha, beta, maximizingPlayer)
            if depth == 0 or game over in position
                return static evaluation of position
        
            if maximizingPlayer
                maxEval = -infinity
                for each child of position
                    eval = minimax(child, depth - 1, alpha, beta false)
                    maxEval = max(maxEval, eval)
                    alpha = max(alpha, eval)
                    if beta <= alpha
                        break
                return maxEval
        
            else
                minEval = +infinity
                for each child of position
                    eval = minimax(child, depth - 1, alpha, beta true)
                    minEval = min(minEval, eval)
                    beta = min(beta, eval)
                    if beta <= alpha
                        break
                return minEval

-Based on the provided rules we update the values of the board moves abnd eval score into the Minimax to choose from all the possible set of boards generated upto a count/depth.


### **Difficulties**
- Reducing the very high run time of program
- Finding the optimum scoring metric(unfortunately this needs more tuning as near the end the tuning fails when only opponent Raichu is left, End up drawing even though there are many opportunities to capture)
- Trying to optimize the raichu code to be compact as per the intention snippet earlier

## **Question 2:**

We are given a dataset of user-generated reviews in the form of training dataset and testing dataset. We have created a 'Naive Bayes classifier', which classifies the reviews into fake or legitimate for 20 hotels in Chicago. The training dataset has labels which tell if the review is 'deceptive' or 'truthful' along with the review.  

### **Bayesian Classifier:**  

To classify the reviews into 'deceptive' and 'truthful', we calculated the probability that a given review is 'truthful' conditioned that it has the words ('P('truthful'|words)'). Or else, it is 'deceptive'.  

- We first get the training data file('deceptive.train.txt') into the form of a dictionary called train_data which has the keys 'labels','objects' and 'classes'. The values for each of the keys is in the form of lists. The values for 'labels' is whether the particular review is 'truthful' or 'deceptive'. In the case of the value for 'objects', it is a list of all the reviews. And finally the value for 'classes' is a list of possible cases i.e 'truthful' or 'deceptive'.  

- We then use string and translate function to preprocess the review sentences (training points) in which we remove the punctuation marks and strip the sentences of any blankspaces at start or end of the line and also lowercase all words in the review  

- We then store the counts of reviews labeled truthful and deceptive accordingly and also the count of total words in both the classes and then use dictionaries to store the frequency of occurrence for each word from the reviews in both the classes  

- We use these for above calculated values for calculating the probability of the given word, conditioned that the review is 'truthful' or 'deceptive'.((P(word|'truthful') or P(word|'deceptive'))  

- The probability of review that contains words (word1 , word2 …) to be ‘truthful’ is proportional to the probability to get the ‘truthful’ , multiplied by a product of probabilities of the words belonging to the ‘truthful’ class.   

- To calculate the word given ‘truthful’ probability , we divide the sum of frequency count of the word in truthful category and a constant with sum of total number of words in the same category and constant into total number of unique words from both the categories   

- We ran a for loop for all the words of each of the review in the test data set. We get the probability that is already calculated for each word and multiply it to the corresponding truthful probability or deceptive probability.((P('truthful') * P(word1|truthful) * P(word2|truthful)...) and (P('deceptive') * P(word1|deceptive) P(word2|deceptive)...))    

- We executed the above calculation first using basic math but for some words ,the word given truthful (or deceptive) probability was going to a very low value and even though the probability wasn’t exactly zero (thus ‘if’ condition did not help) the final probability after multiplication resulted in zero for reviews . Hence used log calculation to get the final probabilities    

- We store each of the above calculated probability into variables called p_true and p_false . Compare them and then we store the result as 'truthful' otherwise it is 'deceptive'.

Result:    

The Result is stored in the form of a list which contains if the given review from the test data set is 'truthful' or 'deceptive'. We are getting a accuracy of 85%.
