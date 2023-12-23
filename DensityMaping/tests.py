import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from scipy.stats import multivariate_normal

# Create a 3D grid
x, y = np.mgrid[-5:5:0.1, -5:5:0.1]
pos = np.dstack((x, y))

# Define parameters for the Gaussian
mean = [0, 0]
covariance = [[1, 0.5], [0.5, 1]]

# Create a multivariate Gaussian distribution
rv = multivariate_normal(mean, covariance)

# Calculate the PDF values
z = rv.pdf(pos)

# Plot the Gaussian in 3D
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.plot_surface(x, y, z, cmap='viridis', edgecolor='k')

ax.set_xlabel('X-axis')
ax.set_ylabel('Y-axis')
ax.set_zlabel('PDF Value')

plt.show()
