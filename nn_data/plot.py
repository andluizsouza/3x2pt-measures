import matplotlib.pyplot as plt
import matplotlib.colors as colors
import numpy as np

def plot (nshells):

	cor = ['r.-', 'g.-', 'b.-', 'y.-', 'c.-']

        plt.figure(figsize = (7,5), dpi = 2048)

        for i in range(nshells):

	        theta, xi = np.loadtxt('nn_z'+str(i+1)+str(i+1)+'.dat', unpack=True, usecols=(0,3))
                plt.semilogx(theta, xi, cor[i], label = r"z-bin " + str(i+1))

	plt.title("Galaxy-galaxy autocorrelation")
        plt.xlabel(r"$\theta$ [arcmin]")
        plt.ylabel(r"$w(\theta)$")
	plt.xlim(theta[0]-5, theta[-1]+5)
        plt.legend(loc = "upper right", shadow = True)
        plt.grid(color = 'k', linestyle = '--', linewidth = 0.2)
        plt.savefig('nn_autocorr.png')

        return

nshells=5
plot(nshells)

