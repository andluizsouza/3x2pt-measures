import numpy as np
import fitsio
# import healpix_util
import healpy as hp
import treecorr
import mpi4py.MPI as MPI

ncpus = None
input_dir = '/home/hcamacho/anderson/treecorr_run_test/'

def compute_SingleMock_SingleBin_NNCorrelation(mock, bin_i, rand, rr, config):

	cat_name = input_dir + 'lens-cat_z'+str(bin_i+1)+'.fits'
	cat = treecorr.Catalog(cat_name, config)

	dd = treecorr.NNCorrelation(config)
	dr = treecorr.NNCorrelation(config)

	print 'Computing NN for z-bin ' + str(bin_i+1)
	dd.process(cat, num_threads=ncpus)
	print 'Computing NR for z-bin ' + str(bin_i+1)
	dr.process(cat, rand, num_threads=ncpus)

	data_name = '/home/anderson/3x2pt/nn_data/nn_z'+str(bin_i+1)+str(bin_i+1)'.dat'
	dd.write(data_name, rr, dr)

	dd.clear()
	dr.clear()	

        return


def compute_SingleMock_AllBin_NNCorrelation(mock, nshells, rand, rr, config):

        for bin_i in range(nshells):
                compute_SingleMock_SingleBin_NNCorrelation(mock, bin_i, rand, rr, config)

	return

def compute_AllMock_NNCorrelation(nmocks, nshells, config):

	rand_name = input_dir + 'ran-cat.fits'
        rand = treecorr.Catalog(rand_name, config)

        print 'Computing RR'
        rr = treecorr.NNCorrelation(config)
        rr.process(rand, num_threads=ncpus)

	for mock in range(nmocks):
		compute_SingleMock_AllBin_NNCorrelation(mock, nshells, rand, rr, config)


	rr.clear()

	return


def main():


	nmocks = 1
	nshells = 1

	config_name = '/home/anderson/3x2pt/config.yaml'
	config = treecorr.read_config(config_name, file_type='yaml')

	compute_AllMock_NNCorrelation(nmocks, nshells, config)

	return


main()
