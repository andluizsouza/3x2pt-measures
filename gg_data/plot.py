import matplotlib.pyplot as plt
import matplotlib.colors as colors
import numpy as np

def plot (nshells):

	cor = ['r.-', 'g.-', 'b.-', 'y.-', 'c.-']


        for i in range(nshells):
		plt.figure(figsize = (6,5), dpi = 2048)
		for j in range(nshells):

			if i < j:
				theta, xip = np.loadtxt('gg_z'+str(i+1)+str(j+1)+'.dat', unpack=True, usecols=(0,3))
			else:
                        	theta, xip = np.loadtxt('gg_z'+str(j+1)+str(i+1)+'.dat', unpack=True, usecols=(0,3))


			plt.loglog(theta, xip, cor[j], label='z-bin ('+str(i+1)+','+str(j+1)+')')

		plt.title("Shear-shear correlation")
        	plt.xlabel(r"$\theta$ [arcmin]")
	        plt.ylabel(r"$\xi_{+}(\theta)$")
        	plt.legend(loc = "upper right", shadow = True)
	        plt.grid(color = 'k', linestyle = '--', linewidth = 0.2)
	        plt.savefig('gg_xip_z'+str(i+1)+'.png')

	
	for i in range(nshells):
                plt.figure(figsize = (6,5), dpi = 2048)
                for j in range(nshells):

                        if i < j:
                                theta, xim = np.loadtxt('gg_z'+str(i+1)+str(j+1)+'.dat', unpack=True, usecols=(0,4))
                        else:
                                theta, xim = np.loadtxt('gg_z'+str(j+1)+str(i+1)+'.dat', unpack=True, usecols=(0,4))


                        plt.loglog(theta, xim, cor[j], label='z-bin ('+str(i+1)+','+str(j+1)+')')

                plt.title("Shear-shear correlation")
                plt.xlabel(r"$\theta$ [arcmin]")
                plt.ylabel(r"$\xi_{-}(\theta)$")
                plt.legend(loc = "upper right", shadow = True)
                plt.grid(color = 'k', linestyle = '--', linewidth = 0.2)
                plt.savefig('gg_xim_z'+str(i+1)+'.png')

        return

plot(5)

