import numpy as np
from numpy import linalg as LA
import cv2
import matplotlib.pyplot as plt
import random
import math

class PointDistributionModel:

    def __init__(self, landmarked_shapes):
        numpy_arrays = []
        for shape in landmarked_shapes:
            numpy_arrays.append(np.asarray(shape))

        self.avg_x = np.mean(numpy_arrays, axis=0)

        for i in range(0, len(numpy_arrays)):
            numpy_arrays[i] = numpy_arrays[i] - self.avg_x

        c_matrix = np.outer(numpy_arrays[0], numpy_arrays[0])
        for i in range(1, len(numpy_arrays)):
            c_matrix += np.outer(numpy_arrays[i], numpy_arrays[i])

        c_matrix = c_matrix / (len(numpy_arrays) - 1)

        # eigh returns (w, v)
        # The normalized selected eigenvector corresponding to the eigenvalue w[i] is the column v[:,i].
        self.eigenvalues, self.eigenvectors = LA.eigh(c_matrix)

    def randomShape(self, seed):
        random.seed(seed)
        new_shape = self.avg_x +( ((random.random()*4-2)*math.sqrt(self.eigenvalues[-1])) * self.eigenvectors[:,-1])
        return new_shape


if __name__ == "__main__":

    # test case
    shapes = [[0.1,0,1,0,1,1,0.2,1],
                [0.2,0.2,1,0,1,1,0,1],
                [0,0,1,0,0.8,0.8,0,1]
              ]

    pdm = PointDistributionModel(shapes)

    print(pdm.randomShape(0))