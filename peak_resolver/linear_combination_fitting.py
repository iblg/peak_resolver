import numpy as np
import pandas as pd
from scipy.optimize import minimize

def residuals(params, C, vectors):
    """
    Calculates the residuals for given parameters and a tuple of vectors.

    Parameters:
    params (array-like): The parameters to be optimized (one for each vector).
    C (pandas.DataFrame): The data to be subtracted from.
    vectors (tuple): A tuple containing pandas DataFrames of arbitrary length.

    Returns:
    numpy.ndarray: The residuals as a NumPy array.
    """
    C_new = C.copy()
    # for param, vector in zip(params, vectors):
    #     C_new -= param * vector

    fit = np.zeros_like(C)
    for param, vector in zip(params, vectors):
        # print(param)
        # print(vector.shape)
        fit += param * vector

    return np.linalg.norm(C_new - fit)

def lin_combination_fitting(target: np.array, vectors: tuple, initial_guess=None, bounds = None, method='Nelder-Mead'):
    """
    Minimizes the residuals of target - linear combination of vectors using scipy.optimize.minimize.

    Parameters:
    target (numpy.array): The data to fitted.
    
    vectors (tuple): A tuple of arbitrary length containing numpy arrays.

    initial_guess: array-like, default None. The initial guess for the coefficients. 
                   If provided, must be same length as the number of fitting vectors.
                   If None, will default to list of ones.

    bounds: list of tuples, one tuple per basis vector.

    method: root-finding algorithm. Default is Nelder-Mead Simplex for its ability to avoid local minima.
            See scipy docs for available choices. Faster algorithms or more robust ones are available.

    Returns:
    dict: A dictionary containing the optimized parameters and minimized residuals.
    """

    num_vectors = len(vectors)
    if initial_guess is None:
        initial_guess = [0.5] * num_vectors  # Provide initial guesses for each parameter
    else:
        pass

    # try:
    result = minimize(residuals, initial_guess, args=(target, vectors), bounds=bounds, method=method)
    # except OptimizeWarning as ow:
        # pass

    return {
        "p": result.x, #return parameters
        "r": result.fun, # return residuals
    }

def calculate_fit(params: list, vecs: tuple):
    fit = np.zeros_like(vecs[0])
    for p, v in zip(params, vecs):
        fit += p * v
    return fit