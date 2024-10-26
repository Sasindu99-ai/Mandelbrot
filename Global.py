import numpy as np

__all__ = ['res', 'width', 'height', 'offset', 'maxIter', 'maxIterLimit', 'appSpeed', 'zoom', 'scale']

# Define the image size
res = width, height = 800, 800
# Define the offset
offset = np.array([1.3 * width, height]) // 2

# Define the maximum number of iterations
maxIter, maxIterLimit = 30, 10000

# App speed
appSpeed = 1 / 4000

# Zoom and scale
zoom, scale = 2.2 / height, 0.993
