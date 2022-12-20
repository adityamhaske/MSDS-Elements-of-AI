# multilayer_perceptron.py: Machine learning implementation of a Multilayer Perceptron classifier from scratch.
#
# Submitted by: [Aditya Sanjay Mhaske] -- [admhaske]
#
# Based on skeleton code by CSCI-B 551 Fall 2022 Course Staff

import numpy as np
from utils import identity, sigmoid, tanh, relu, softmax, cross_entropy, one_hot_encoding


class MultilayerPerceptron:
    """
    A class representing the machine learning implementation of a Multilayer Perceptron classifier from scratch.

    Attributes:
        n_hidden
            An integer representing the number of neurons in the one hidden layer of the neural network.

        hidden_activation
            A string representing the activation function of the hidden layer. The possible options are
            {'identity', 'sigmoid', 'tanh', 'relu'}.

        n_iterations
            An integer representing the number of gradient descent iterations performed by the fit(X, y) method.

        learning_rate
            A float representing the learning rate used when updating neural network weights during gradient descent.

        _output_activation
            An attribute representing the activation function of the output layer. This is set to the softmax function
            defined in utils.py.

        _loss_function
            An attribute representing the loss function used to compute the loss for each iteration. This is set to the
            cross_entropy function defined in utils.py.

        _loss_history
            A Python list of floats representing the history of the loss function for every 20 iterations that the
            algorithm runs for. The first index of the list is the loss function computed at iteration 0, the second
            index is the loss function computed at iteration 20, and so on and so forth. Once all the iterations are
            complete, the _loss_history list should have length n_iterations / 20.

        _X
            A numpy array of shape (n_samples, n_features) representing the input data used when fitting the model. This
            is set in the _initialize(X, y) method.

        _y
            A numpy array of shape (n_samples, n_outputs) representing the one-hot encoded target class values for the
            input data used when fitting the model.

        _h_weights
            A numpy array of shape (n_features, n_hidden) representing the weights applied between the input layer
            features and the hidden layer neurons.

        _h_bias
            A numpy array of shape (1, n_hidden) representing the weights applied between the input layer bias term
            and the hidden layer neurons.

        _o_weights
            A numpy array of shape (n_hidden, n_outputs) representing the weights applied between the hidden layer
            neurons and the output layer neurons.

        _o_bias
            A numpy array of shape (1, n_outputs) representing the weights applied between the hidden layer bias term
            neuron and the output layer neurons.

    Methods:
        _initialize(X, y)
            Function called at the beginning of fit(X, y) that performs one-hot encoding for the target class values and
            initializes the neural network weights (_h_weights, _h_bias, _o_weights, and _o_bias).

        fit(X, y)
            Fits the model to the provided data matrix X and targets y.

        predict(X)
            Predicts class target values for the given test data matrix X using the fitted classifier model.
    """

    def __init__(self, n_hidden = 16, hidden_activation = 'sigmoid', n_iterations = 1000, learning_rate = 0.01):
        # Create a dictionary linking the hidden_activation strings to the functions defined in utils.py
        activation_functions = {'identity': identity, 'sigmoid': sigmoid, 'tanh': tanh, 'relu': relu}

        # Check if the provided arguments are valid
        if not isinstance(n_hidden, int) \
                or hidden_activation not in activation_functions \
                or not isinstance(n_iterations, int) \
                or not isinstance(learning_rate, float):
            raise ValueError('The provided class parameter arguments are not recognized.')

        # Define and setup the attributes for the MultilayerPerceptron model object
        self.n_hidden = n_hidden
        self.hidden_activation = activation_functions[hidden_activation]
        self.n_iterations = n_iterations
        self.learning_rate = learning_rate
        self._output_activation = softmax
        self._loss_function = cross_entropy
        self._loss_history = []
        self._X = None
        self._y = None
        self._h_weights = None
        self._h_bias = None
        self._o_weights = None
        self._o_bias = None

    def _initialize(self, X, y):
        """
        Function called at the beginning of fit(X, y) that performs one hot encoding for the target class values and
        initializes the neural network weights (_h_weights, _h_bias, _o_weights, and _o_bias).

        Args:
            X: A numpy array of shape (n_samples, n_features) representing the input data.
            y: A numpy array of shape (n_samples,) representing the true class values for each sample in the input data.

        Returns:
            None.
        """
        self._X = X
        
        self._y = one_hot_encoding(y)

        ic=X.shape[0]

        fc=X.shape[1]

        oc=np.max(y)

'''
n order to proceed we need to improve the notation we have been using. That for, for each layer  1≥𝑙≥𝐿 , the activations and outputs are calculated as:

L𝑙𝑗=∑𝑖𝑤𝑙𝑗𝑖𝑥𝑙𝑖=𝑤𝑙𝑗,0𝑥𝑙0+𝑤𝑙𝑗,1𝑥𝑙1+𝑤𝑙𝑗,2𝑥𝑙2+...+𝑤𝑙𝑗,𝑛𝑥𝑙𝑛,
 
𝑌𝑙𝑗=𝑔𝑙(L𝑙𝑗),
 
{𝑦𝑖,𝑥𝑖1,…,𝑥𝑖𝑝}𝑛𝑖=1
 
where:

𝑦𝑙𝑗  is the  𝑗− th output of layer  𝑙 ,
𝑥𝑙𝑖  is the  𝑖 -th input to layer  𝑙 ,
𝑤𝑙𝑗𝑖  is the weight of the  𝑗 -th neuron connected to input  𝑖 ,
L𝑙𝑗  is called net activation, and
𝑔𝑙(⋅)  is the activation function of layer  𝑙 .
 '''
        
        self._h_weights=np.random.rand(fc,self.n_hidden)

        self._h_bias=np.random.randn(self.n_hidden)
'''
It was important to carry out several experiments using various parameter values in order to identify the optimal ones. 
The graphs below show every test run to determine the multilayer perceptron's ideal configuration. 
'''

        self._o_weights=np.random.rand(self.n_hidden,oc+1)

        self._o_bias=np.random.randn(oc+1)
     
'''
These tests were crucial for choosing the best options and assuring the highest level of accuracy. 
The graph was manually created, but you may alter the settings and take note of the outcomes. 
Different activation mechanisms and the number of neurons in each layer are tested.
'''



        np.random.seed(42)

        # https://www.kaggle.com/code/vitorgamalemos/multilayer-perceptron-from-scratch
        # raise NotImplementedError('This function must be implemented by the student.')

    def fit(self, X, y):
        """
        Fits the model to the provided data matrix X and targets y and stores the cross-entropy loss every 20
        iterations.

        Args:
            X: A numpy array of shape (n_samples, n_features) representing the input data.
            y: A numpy array of shape (n_samples,) representing the true class values for each sample in the input data.

        Returns:
            None.
        """
        # https://github.com/KirillShmilovich/MLP-Neural-Network-From-Scratch/blob/master/MLP.ipynb
        # https://www.codingame.com/playgrounds/9487/deep-learning-from-scratch---theory-and-implementation/multi-layer-perceptrons

        self._initialize(X, y)

        for i in range(self.n_iterations):

            hido=np.dot(self._X,self._h_weights)+self._h_bias

            hido_a=self.hidden_activation(hido)  #Activation output --> hidden activation

            pa=np.dot(hido_a,self._o_weights)+self._o_bias

            pa_a=self._output_activation(pa) #Activation output --> output activation

            # part 1 of initialization 

            ape=pa_a-self._y

            alpha=self._output_activation(pa,derivative=True)

            ahd=self._output_activation(hido,derivative=True)

            apehd=np.dot(pa_a,self._o_weights.T)

            alphaopt = ape * alpha

            alphahid = apehd * ahd

            self._h_weights=self._h_weights-(self.learning_rate*np.dot(alphahid.T,self._X))/len(self._X)

            self._o_weights=self._o_weights-(self.learning_rate*np.dot(alphaopt.T,hido_a))/len(self._X)

        return


        #raise NotImplementedError('This function must be implemented by the student.')

    def predict(self, X):
        """
        Predicts class target values for the given test data matrix X using the fitted classifier model.

        Args:
            X: A numpy array of shape (n_samples, n_features) representing the test data.

        Returns:
            A numpy array of shape (n_samples,) representing the predicted target class values for the given test data.
        """
        hido = np.dot(self._X,self._h_weights)+self._h_bias

        hidoa = self.hidden_activation(hido)

        pa = np.dot(hido,self._o_weights)+self._o_bias

        pa_a = self._output_activation(pa)

        eval = []

        for x in pa_a:

            eval.append(np.argmax(x))
        
        return eval


        # raise NotImplementedError('This function must be implemented by the student.')
