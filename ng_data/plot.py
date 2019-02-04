import matplotlib.pyplot as plt
import matplotlib.colors as colors
import numpy as np

def plot (nshells):

	cor = ['r.-', 'g.-', 'b.-', 'y.-', 'c.-']


        for i in range(nshells):
		plt.figure(figsize = (6,5), dpi = 2048)
		for j in range(nshells):

			theta, gamma = np.loadtxt('ng_z'+str(i+1)+str(j+1)+'.dat', unpack=True, usecols=(0,3))
			plt.loglog(theta, gamma, cor[j], label='z-bin ('+str(i+1)+','+str(j+1)+')')

		plt.title("Galaxy-shear correlation")
        	plt.xlabel(r"$\theta$ [arcmin]")
	        plt.ylabel(r"$\gamma_{t}(\theta)$")
        	plt.legend(loc = "upper right", shadow = True)
	        plt.grid(color = 'k', linestyle = '--', linewidth = 0.2)
	        plt.savefig('ng_gt_z'+str(i+1)+'.png')

        return

plot(5)

