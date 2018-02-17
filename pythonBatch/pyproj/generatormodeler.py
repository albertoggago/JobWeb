#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" Clase unique GeneratorModeler """
import json
import numpy
import pandas
#from scipy.sparse import eye, lil_matrix, coo_matrix, vstack
from scipy.sparse import coo_matrix


from pyproj.logger import Logger


class GeneratorModeler(object):
    """ Initialize class """

    logger = None
    config = None
    dataframe = None
    dataframe_matrix = None

    def __init__(self, fileConfig, level_log):
        self.logger = Logger(self.__class__.__name__, level_log).get()
        config_text = open(fileConfig, "r").read()
        allconfig = json.loads(config_text)
        self.config = allconfig

    def generate_dataframe(self, path, file_ds, file_matrix):
        """ Generate dataframe using data of web"""
        self.logger.info("Generate DataFrame")
        self.dataframe = pandas.read_csv(path+file_ds)
        self.dataframe_matrix = self.load_sparse_matrix(path+file_matrix)
        out_put = []
        out_put.append(self.dataframe.shape[0])
        out_put.append(self.dataframe_matrix.get_shape()[0])
        return out_put

    def save_sparse_matrix(self, dataset, filename):
        """ With a DataSet save the sparse matrix to file """
        self.logger.info("Save sparse matrix")
        dataset_to_coo = dataset.tocoo()
        rows = dataset_to_coo.row
        cols = dataset_to_coo.col
        data = dataset_to_coo.data
        shape = dataset_to_coo.shape
        self.logger.info("rows: %d, cols %d", rows, cols)
        numpy.savez(filename, row=rows, col=cols, data=data, shape=shape)

    def load_sparse_matrix(self, filename):
        """ With a path load the sparse matrix to file return a sparse matrix """
        self.logger.info("Load sparse matrix")
        self.logger.info("filename %s", filename)
        load_file = numpy.load(filename)
        return coo_matrix((load_file['data'], (load_file['row'], load_file['col'])),\
                        shape=load_file['shape'])
