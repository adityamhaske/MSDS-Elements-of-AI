# k_nearest_neighbors.py: Machine learning implementation of a K-Nearest Neighbors classifier from scratch.
#
# Submitted by: [Aditya Sanjay Mhaske] -- [admhaske]
#
# Based on skeleton code by CSCI-B 551 Fall 2022 Course Staff

import numpy as np
from utils import euclidean_distance, manhattan_distance


class KNearestNeighbors:
    """
    A class representing the machine learning implementation of a K-Nearest Neighbors classifier from scratch.

    Attributes:
        n_neighbors
            An integer representing the number of neighbors a sample is compared with when predicting target class
            values.

        weights
            A string representing the weight function used when predicting target class values. The possible options are
            {'uniform', 'distance'}.

        _X
            A numpy array of shape (n_samples, n_features) representing the input data used when fitting the model and
            predicting target class values.

        _y
            A numpy array of shape (n_samples,) representing the true class values for each sample in the input data
            used when fitting the model and predicting target class values.

        _distance
            An attribute representing which distance metric is used to calculate distances between samples. This is set
            when creating the object to either the euclidean_distance or manhattan_distance functions defined in
            utils.py based on what argument is passed into the metric parameter of the class.

    Methods:
        fit(X, y)
            Fits the model to the provided data matrix X and targets y.

        predict(X)
            Predicts class target values for the given test data matrix X using the fitted classifier model.
    """

    def __init__(self, n_neighbors = 5, weights = 'uniform', metric = 'l2'):
        # Check if the provided arguments are valid
        if weights not in ['uniform', 'distance'] or metric not in ['l1', 'l2'] or not isinstance(n_neighbors, int):
            raise ValueError('The provided class parameter arguments are not recognized.')

        # Define and setup the attributes for the KNearestNeighbors model object
        self.n_neighbors = n_neighbors
        self.weights = weights
        self._X = None
        self._y = None
        self._distance = euclidean_distance if metric == 'l2' else manhattan_distance

    def fit(self, X, y):
        """
        Fits the model to the provided data matrix X and targets y.

        Args:
            X: A numpy array of shape (n_samples, n_features) representing the input data.
            y: A numpy array of shape (n_samples,) representing the true class values for each sample in the input data.

        Returns:
            None.
        """
        self._X = X
        self._y = y

        return

        # raise NotImplementedError('This function must be implemented by the student.')

    def predict(self, X):
        """
        Predicts class target values for the given test data matrix X using the fitted classifier model.

        Args:
            X: A numpy array of shape (n_samples, n_features) representing the test data.

        Returns:
            A numpy array of shape (n_samples,) representing the predicted target class values for the given test data.
        """

        output = []
        for i in range(len(X)):
            d1 = []
            v = []
            for j in range(len(self._X)):
                cd = {}
                d2 = euclidean_distance(self._X[j], X[i])
                #Euclidean Distance = sqrt(sum i to N (x1_i — x2_i)²)

                d1.append([d2, j])
            d1.sort()
            d1 = d1[0:self.n_neighbors]
            #Manhatten Distance = sum for i to N sum || X1i – X2i ||
            cd = {}
            if self.weights == 'd1':
                uv = np.unique(self._y)
                #Getting K nearest neighbors by sorting the euclidean distances
                for key in uv:
                    cd[key] = 0  
                # Predicting or classifying the new data point
                for d2, index in d1:
                    if d2 == 0:
                       cd[self._y[index]] += 1
                    else:
                       cd[self._y[index]] += 1/d2
                output.append(max(cd, key=cd.get))
                #Two methods exist for selecting the K value. 
                #Use cross-validation for hyperparameter tuning by taking the sqrt of the number of data points (a) and choosing the K value that produced the least amount of error (b). 
                #K can be chosen from a range, such as (1, 21).
            else:
                for a, j in d1:
                    v.append(self._y[j])
                ans = Counter(v).most_common(1)[0][0]
                output.append(ans)
        return output

        # https://towardsdatascience.com/how-to-build-knn-from-scratch-in-python-5e22b8920bd2
        # raise NotImplementedError('This function must be implemented by the student.')
