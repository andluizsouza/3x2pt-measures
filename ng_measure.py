import numpy as np
import fitsio
# import healpix_util
import healpy as hp
import treecorr
import mpi4py.MPI as MPI

ncpus = 64

def compute_SingleMock_SingleBin_NNCorrelation(mock, bin_i, rand, rr, config):

	cat_name = '/home/hcamacho/lens_s1_z'+str(bin_i+1)+'_c1.fits'
	cat = treecorr.Catalog(cat_name, config)

	dd = treecorr.NNCorrelation(config)
	dr = treecorr.NNCorrelation(config)

	print 'Computing NN for z-bin ' + str(bin_i+1)
	dd.process(cat, num_threads=ncpus)
	print 'Computing NR for z-bin ' + str(bin_i+1)
	dr.process(cat, rand, num_threads=ncpus)

	data_name = '/home/anderson/3x2pt/nn_data/nn_s1_z'+str(bin_i+1)+'_c1.dat'
	dd.write(data_name, rr, dr)

	dd.clear()
	dr.clear()	

        return


def compute_SingleMock_AllBin_NNCorrelation(mock, nshells, rand, rr, config):

        for bin_i in range(nshells):
                compute_SingleMock_SingleBin_NNCorrelation(mock, bin_i, rand, rr, config)

	return

def compute_AllMock_NNCorrelation(nmocks, nshells, config):

	rand_name = '/home/hcamacho/ran_c1.fits'
	#rand_name = '/home/hcamacho/lens_s1_z1_c1.fits'
        rand = treecorr.Catalog(rand_name, config)

        print 'Computing RR'
        rr = treecorr.NNCorrelation(config)
        rr.process(rand, num_threads=ncpus)

	"""

	# Parallel version

        # mpi4py has the notion of a "communicator" - a collection of processors all operating together, usually on the same program.
        # Each processor in the communicator is identified by a number, its rank,  We'll use that number to split the tasks
        comm = MPI.COMM_WORLD

        # find out which number processor this particular instance is, and how many there are in total
        rank = comm.Get_rank()
        size = comm.Get_size()

        # the enumerate function gives us a number i in addition to the task. 
        # (In this specific case i is the same as task! But that's not true usually)

        task_list = np.arange(nmocks)

	


        for i, task in enumerate(task_list):
                # This is how we split up the jobs.
                # The % sign is a modulus, and the "continue" means "skip the rest of this bit and go to the next time through the loop"
                # If we had e.g. 4 processors, this would mean that
                # processor zero did tasks 0, 4, 8, 12, 16, ...
                # and processor one did tasks 1, 5, 9, 13, 17, ... and do on.

                if i%size != rank: continue
                # print "Task number %d (%d) being done by processor %d of %d" % (i, task, rank, size
                compute_SingleMock_AllBin_NNCorrelation(task, nshells, rand, rr, config)

	"""

	for mock in range(nmocks):
		compute_SingleMock_AllBin_NNCorrelation(mock, nshells, rand, rr, config)


	rr.clear()

	return


def compute_SingleMock_AllPair_GGCorrelation(nshells, config):	


	for bin_i in range(nshells):
		cat_i_name = '/home/hcamacho/src_s1_z'+str(bin_i+1)+'_c1.fits'
		cat_i = treecorr.Catalog(cat_i_name, config)
		for bin_j in range(bin_i, nshells):
			compute_SingleMock_SinglePair_GGCorrelation(cat_i, bin_i, bin_j, config)

	return

def compute_SingleMock_SinglePair_GGCorrelation(cat_i, bin_i, bin_j, config):

	if bin_i == bin_j:
		gg = treecorr.GGCorrelation(config)
	        gg.process(cat_i, num_threads=ncpus)

	else:
		cat_j_name = '/home/hcamacho/src_s1_z'+str(bin_j+1)+'_c1.fits'
        	cat_j = treecorr.Catalog(cat_j_name, config)

		gg = treecorr.GGCorrelation(config)
	        gg.process(cat_i, cat_j, num_threads=ncpus)


	data_name = '/home/anderson/3x2pt/gg_data/gg_s1_z'+str(bin_i+1)+str(bin_j+1)+'_c1.dat'
	gg.write(data_name)
        gg.clear()

	return


def compute_SingleMock_AllPair_NGCorrelation(nshells, config):


        for bin_j in range(nshells):
                cat_j_name = '/home/hcamacho/src_s1_z'+str(bin_j+1)+'_c1.fits'
                cat_j = treecorr.Catalog(cat_j_name, config)
                for bin_i in range(nshells):
                        compute_SingleMock_SinglePair_NGCorrelation(cat_j, bin_i, bin_j, config)

        return

def compute_SingleMock_SinglePair_NGCorrelation(cat_j, bin_i, bin_j, config):

	cat_i_name = '/home/hcamacho/lens_s1_z'+str(bin_i+1)+'_c1.fits'
        cat_i = treecorr.Catalog(cat_i_name, config)

        ng = treecorr.NGCorrelation(config)
	ng.process(cat_i, cat_j, num_threads=ncpus)


        data_name = '/home/anderson/3x2pt/ng_data/ng_s1_z'+str(bin_i+1)+str(bin_j+1)+'_c1.dat'
        ng.write(data_name)
        ng.clear()

        return



def main():


	nmocks = 1
	nshells = 5

	config_name = '/home/anderson/3x2pt/config.yaml'
	config = treecorr.read_config(config_name, file_type='yaml')

	#compute_AllMock_NNCorrelation(nmocks, nshells, config)
	#compute_SingleMock_AllPair_GGCorrelation(nshells, config)
	compute_SingleMock_AllPair_NGCorrelation(nshells, config)


	return


main()
