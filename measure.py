import numpy as np
import fitsio
import healpy as hp
import treecorr

ncpus = None
input_dir = '/home/hcamacho/anderson/treecorr_run_test/'
output_dir = '/home/anderson/3x2pt/'


def compute_SingleBin_NNCorrelation(bin_i, rand, rr, config):

        cat_name = input_dir + 'lens-cat_z'+str(bin_i+1)+'.fits'
        cat = treecorr.Catalog(cat_name, config)

        dd = treecorr.NNCorrelation(config)
        dr = treecorr.NNCorrelation(config)

        dd.process(cat, num_threads=ncpus)
        dr.process(cat, rand, num_threads=ncpus)

        data_name = output_dir + 'nn_data/nn_z'+str(bin_i+1)+str(bin_i+1)+'.dat'
        dd.write(data_name, rr, dr)

        dd.clear()
        dr.clear()

        return


def compute_AllBin_NNCorrelation(nshells, config):

        rand_name = input_dir + 'ran-cat.fits'
        rand = treecorr.Catalog(rand_name, config)
        rr = treecorr.NNCorrelation(config)
        rr.process(rand, num_threads=ncpus)

        for bin_i in range(nshells):
                compute_SingleBin_NNCorrelation(bin_i, rand, rr, config)

	rr.clear()

        return

def compute_AllPair_NGCorrelation(nshells, config):


        for bin_j in range(nshells):
                cat_j_name = input_dir + 'src-cat_z'+str(bin_j+1)+'.fits'
                cat_j = treecorr.Catalog(cat_j_name, config)
                for bin_i in range(nshells):
                        compute_SinglePair_NGCorrelation(cat_j, bin_i, bin_j, config)

        return



def compute_SinglePair_NGCorrelation(cat_j, bin_i, bin_j, config):

        cat_i_name = input_dir + 'lens-cat_z'+str(bin_i+1)+'.fits'
        cat_i = treecorr.Catalog(cat_i_name, config)

        ng = treecorr.NGCorrelation(config)
        ng.process(cat_i, cat_j, num_threads=ncpus)


        data_name = output_dir + 'ng_data/ng_z'+str(bin_i+1)+str(bin_j+1)+'.dat'
        ng.write(data_name)
        ng.clear()

        return

def compute_AllPair_GGCorrelation(nshells, config):


        for bin_i in range(nshells):
                cat_i_name = input_dir + 'src-cat_z'+str(bin_i+1)+'.fits'
                cat_i = treecorr.Catalog(cat_i_name, config)
                for bin_j in range(bin_i, nshells):
                        compute_SinglePair_GGCorrelation(cat_i, bin_i, bin_j, config)

        return

def compute_SinglePair_GGCorrelation(cat_i, bin_i, bin_j, config):

        if bin_i == bin_j:
                gg = treecorr.GGCorrelation(config)
                gg.process(cat_i, num_threads=ncpus)

        else:
                cat_j_name = input_dir + 'src-cat_z'+str(bin_j+1)+'.fits'
                cat_j = treecorr.Catalog(cat_j_name, config)

                gg = treecorr.GGCorrelation(config)
                gg.process(cat_i, cat_j, num_threads=ncpus)


        data_name = output_dir + 'gg_data/gg_z'+str(bin_i+1)+str(bin_j+1)+'.dat'
        gg.write(data_name)
        gg.clear()

        return

def main():


        nshells = 5

        config_name = '/home/anderson/3x2pt/config.yaml'
        config = treecorr.read_config(config_name, file_type='yaml')

	compute_AllBin_NNCorrelation(nshells, config)	
        compute_AllPair_NGCorrelation(nshells, config)
        compute_AllPair_GGCorrelation(nshells, config)

        return


main()

