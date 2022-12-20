# admhaske-a4

## K- Nearest Neighbors Classification
Q. -> In the machine learning world, k-nearest neighbors is a type of non-parametric supervised machine learning 
algorithm  that  is  used  for  both  classification  and  regression  tasks.  For  classification,  the  principle  behind  k-
nearest neighbors is to find k training samples that are closest in distance to a new sample in the test dataset, 
and then make a prediction based on those samples.

### Problem Solving 
1. The Euclidean distance formula says:

d = √[ (x
2
 – x
1
)2 + (y
2
 – y
1
)2]

where,

(x
1
, y
1
) are the coordinates of one point.
(x
2
, y
2
) are the coordinates of the other point.
d is the distance between (x
1
, y
1
) and (x
2
, y
2
).

2. Manhattan Distance

The Manhattan distance as the sum of absolute differences

ManhattanDistance [{a, b, c}, {x, y, z}]

Abs [a − x] + Abs [b − y] + Abs [c − z]


The k-Nearest Neighbors algorithm, sometimes known as KNN, is a fairly straightforward method. It is saved the full training dataset. The k-most comparable records from the training dataset to a new record are then found when a prediction is needed. On the basis of these neighbors, a concise prognosis is made.

The separation d between each training observation and x is being computed. The points in the dataset that are closest to x will be designated "k." K is often strange to avoid a tie scenario.

For each class, the conditional probability—or the proportion of points in a collection having that specific class label—is now determined.

## Multilayer Perceptron Classification

Q. -> we will specifically be focusing on multilayer perceptron neural networks that are feed-
forward, fully-connected, and have exactly three layers: an input layer, a hidden layer, and an output layer.
A feedforward fully-connected network is one where each node in one layer connects with a certain weight
to every node in the following layer. 

### Problem Solving
Theory
Multiple layers of a set of perceptron are layered together to create a model in a sort of network known as a multi-layer perceptron. Let's start with the fundamental unit of this network, the perceptron, before we go on to the idea of a layer and many perceptrons. Consider perceptron/neuron as a linear model that accepts various inputs and outputs. In our situation, the perceptron is a linear model that produces an output by taking a number of inputs, multiplying them by weights, and adding a bias term.

1. Relu: 
will use Rectified Linear Units (ReLu), one of the most used activation functions. ReLU is a straightforward function that returns zero for every input value that is less than zero and the same value for values that are larger than zero.

2. Sigmoid:
a neural network's sigmoid unit. The output of this unit will always range between 0 and 1 when the activation function of a neuron is a sigmoid function. The output of this unit would also be a non-linear function of the weighted sum of the inputs since the sigmoid is a non-linear function.

3. Cross Entropy Loss:
The cross-entropy loss function is an optimization function that is used for training classification models which classify the data by predicting the probability (value between 0 and 1) of whether the data belong to one class or another

4. One hot encoder: 
One hot encoding, which improves predictions and classification accuracy of a mode, is the crucial process of changing the categorical data variables to be fed to machine and deep learning algorithms.

5. Softmax:
softmax function is given as, ∂pi∂aj={pi(1−pj)ifi=j−pj.

### Problems Faced
1. Difficulties in back propogation implementation
2. Multilayer perceptron classification from scratch is challening with consideration of all parameters
