# utils.py: Utility file for implementing helpful utility functions used by the ML algorithms.
#
# Submitted by: [Aditya Sanjay Mhaske] -- [admhaske]
#
# Based on skeleton code by CSCI-B 551 Fall 2022 Course Staff

import numpy as np


def euclidean_distance(x1, x2):
    """
    Computes and returns the Euclidean distance between two vectors.

    Args:
        x1: A numpy array of shape (n_features,).
        x2: A numpy array of shape (n_features,).
    """
    e1 = np.square(x1-x2)
    e2 = np.sum(e1)
    e = np.sqrt(e1)
    return e

    # Reference: https://www.folkstalk.com/tech/calculate-euclidean-distance-in-python-with-code-examples/#:~:text=What's%20the%20distance%20in%20Python,(z%2Dc)%5E2%20%5D.
    # raise NotImplementedError('This function must be implemented by the student.')


def manhattan_distance(x1, x2):
    """
    Computes and returns the Manhattan distance between two vectors.

    Args:
        x1: A numpy array of shape (n_features,).
        x2: A numpy array of shape (n_features,).
    """
    m = np.sum(np.abs(x1-x2))
    return m

    #reference: https://www.statology.org/manhattan-distance-python/
    # raise NotImplementedError('This function must be implemented by the student.')


def identity(x, derivative = False):
    """
    Computes and returns the identity activation function of the given input data x. If derivative = True,
    the derivative of the activation function is returned instead.

    Args:
        x: A numpy array of shape (n_samples, n_hidden).
        derivative: A boolean representing whether or not the derivative of the function should be returned instead.
    """
    if derivative:
        return 1
    return x

    # raise NotImplementedError('This function must be implemented by the student.')


def sigmoid(x, derivative = False):
    """
    Computes and returns the sigmoid (logistic) activation function of the given input data x. If derivative = True,
    the derivative of the activation function is returned instead.

    Args:
        x: A numpy array of shape (n_samples, n_hidden).
        derivative: A boolean representing whether or not the derivative of the function should be returned instead.
    """
    s=1/(1+np.exp(-x))
    if derivative:
       sd=s*(1-s)
       return sd
    return s

    # https://www.statology.org/sigmoid-function-python/
    # raise NotImplementedError('This function must be implemented by the student.')


def tanh(x, derivative = False):
    """
    Computes and returns the hyperbolic tangent activation function of the given input data x. If derivative = True,
    the derivative of the activation function is returned instead.

    Args:
        x: A numpy array of shape (n_samples, n_hidden).
        derivative: A boolean representing whether or not the derivative of the function should be returned instead.
    """

    if (derivative == False):
        val1 = np.tanh(x)
        return val1
    else:
        val2 = (1 - (tanh(x) ** 2))
        return val2

    #raise NotImplementedError('This function must be implemented by the student.')


def relu(x, derivative = False):
    """
    Computes and returns the rectified linear unit activation function of the given input data x. If derivative = True,
    the derivative of the activation function is returned instead.

    Args:
        x: A numpy array of shape (n_samples, n_hidden).
        derivative: A boolean representing whether or not the derivative of the function should be returned instead.
    """
    if (derivative == False):
        val3 = np.maximum(0,x)
        return val3
    else:
        x[x > 0] = 1
        x[x <= 0] = 0
        return x

    # https://stackoverflow.com/questions/46411180/implement-relu-derivative-in-python-numpy
    # raise NotImplementedError('This function must be implemented by the student.')


def softmax(x, derivative = False):
    x = np.clip(x, -1e100, 1e100)
    if not derivative:
        c = np.max(x, axis = 1, keepdims = True)
        return np.exp(x - c - np.log(np.sum(np.exp(x - c), axis = 1, keepdims = True)))
    else:
        return softmax(x) * (1 - softmax(x))


def cross_entropy(y, p):
    """
    Computes and returns the cross-entropy loss, defined as the negative log-likelihood of a logistic model that returns
    p probabilities for its true class labels y.

    Args:
        y:
            A numpy array of shape (n_samples, n_outputs) representing the one-hot encoded target class values for the
            input data used when fitting the model.
        p:
            A numpy array of shape (n_samples, n_outputs) representing the predicted probabilities from the softmax
            output activation function.
    """

    ce_1=(p + pow(10, -7))
    ce_2=(y * np.log(ce_1))
    ce_3=-np.mean(ce_2)
    return ce_3
    # https://vitalflux.com/cross-entropy-loss-explained-with-python-examples/
    #raise NotImplementedError('This function must be implemented by the student.')


def one_hot_encoding(y):
    """
    Converts a vector y of categorical target class values into a one-hot numeric array using one-hot encoding: one-hot
    encoding creates new binary-valued columns, each of which indicate the presence of each possible value from the
    original data.

    Args:
        y: A numpy array of shape (n_samples,) representing the target class values for each sample in the input data.

    Returns:
        A numpy array of shape (n_samples, n_outputs) representing the one-hot encoded target class values for the input
        data. n_outputs is equal to the number of unique categorical class values in the numpy array y.
    """
    xm=np.max(y)
    xar=[[0 for x in range(xm+1)] for y in range(np.shape(y)[0])]
    for i in range(np.shape(y)[0]):
        xar[i][y[i]]=1
    return xar

    # https://www.statology.org/one-hot-encoding-in-python/
    #raise NotImplementedError('This function must be implemented by the student.')
