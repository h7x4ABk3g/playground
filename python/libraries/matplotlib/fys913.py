# Physics 1 exercise 9.13

import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import curve_fit
plt.style.use("ggplot")
X = [0.10, 0.20, 0.30, 0.40, 0.50] #Dataset
Y = [0.50, 0.95, 1.5, 2.0, 2.6]

#Function type
def f(a, b):
    return b * a

#Regression
L, V = curve_fit(f, X, Y)

print(L)
x = np.linspace(0,0.6,700)
plt.scatter(X,Y)
plt.plot(x, f(x, *L), color="b")
plt.show()
