#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" Clase unique GeneratorModeler """
import json
import numpy
import pandas
#from scipy.sparse import eye, lil_matrix, coo_matrix, vstack
from scipy.sparse import coo_matrix, eye
from sklearn.model_selection import train_test_split

from pyproj.logger import Logger

from pyproj.models.blockdata import BlockData


class ModelsGenerator(object):
    """ Initialize class """

    logger = None
    config = None

    def __init__(self, fileConfig, level_log):
        self.logger = Logger(self.__class__.__name__, level_log).get()
        config_text = open(fileConfig, "r").read()
        allconfig = json.loads(config_text)
        self.config = allconfig


    def generate_dataframe(self, path, file_ds, file_matrix=""):
        """ Generate dataframe using data of web"""
        self.logger.info("Generate DataFrame")
        dataframe = pandas.read_csv(path+file_ds)
        if file_matrix != "":
            dataframe_matrix = self.load_sparse_matrix(path+file_matrix)
            return BlockData(dataframe, dataframe_matrix)

    def save_sparse_matrix(self, dataset, filename):
        """ With a DataSet save the sparse matrix to file """
        self.logger.info("Save sparse matrix")
        if dataset is None:
            self.logger.error("Dataset Error")
            return None
        else:
            dataset_to_coo = dataset.tocoo()
            rows = dataset_to_coo.row
            cols = dataset_to_coo.col
            data = dataset_to_coo.data
            shape = dataset_to_coo.shape
            self.logger.info("rows: %d, cols %d", rows, cols)
            numpy.savez(filename, row=rows, col=cols, data=data, shape=shape)
            out_put = []
            out_put.append({"rows":rows, "cols":cols})
            return output

    def load_sparse_matrix(self, filename):
        """ With a path load the sparse matrix to file return a sparse matrix """
        self.logger.info("Load sparse matrix")
        self.logger.info("filename %s", filename)
        load_file = numpy.load(filename)
        return coo_matrix((load_file['data'], (load_file['row'], load_file['col'])),\
                        shape=load_file['shape'])

    def generate_test_train(self, test_size=0.2):
        """ generate train and test """
        self.df_train, self.df_test = train_test_split(self.dataframe\
                                                       , test_size=test_size, random_state=0)
        self.df_train_matrix = eye(0)
        self.df_test_matrix = eye(0)
        for row_name in self.df_train.index:
            row = self.df_matrix.getrow(row_name)
            self.df_train_matrix = vstack([self.df_train_matrix, row])
        for row_name in self.df_test.index:
            row = self.df_matrix.getrow(row_name)
            self.df_test_matrix = vstack([self.df_test_matrix, row])
        self.logger.info("CREATE DF TRAIN %s %s", self.df_train.shape[0],\
                                                  self.df_train.shape[1])
        self.logger.info("CREATE DF TEST  %s %s", self.df_test.shape[0],\
                                                  self.df_test.shape[1])
        self.logger.info("CREATE MATRIX TRAIN %s %s", self.df_train_matrix.shape[0],\
                                                      self.df_train_matrix.shape[1])
        self.logger.info("CREATE MATRIX TRAIN %s %s", self.df_train_matrix.shape[0],\
                                                      self.df_train_matrix.shape[1])
