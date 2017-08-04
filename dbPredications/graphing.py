# Noah M. Schumacher
#### Trial graphing script


import numpy as np
import matplotlib.pyplot as plt

t = np.arange(0., 5., .2)

print(t)

#### Plotting three functions in same line
#plt.plot(t, t, 'r--', t, t**2, 'bs', t, t**3, 'g^')
#plt.show()

#### Trying to put threee thigns on same plot
plt.plot(t, t, 'r', label='linear')
plt.plot(t, t**2, 'b', label='quadratic')
plt.plot(t, t**3, 'g', label='3rd')

plt.xticks(np.arange(0, 5, .5))
plt.xlabel("X")
plt.ylabel("Y")
plt.title("3 Plots")
plt.legend()

plt.show()
