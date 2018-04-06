#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" RUN all models using data of data base"""


import datetime
import logging

from pyproj.models.modelsgenerator import ModelsGenerator

if __name__ == '__main__':
    print "## INFO ## inicio: {0}".format(datetime.datetime.now())
    MODELS_GENERATOR = ModelsGenerator("config/configModels.json", logging.INFO)
    ELEMENTS_READ = MODELS_GENERATOR.generate_dataframe("data/", "dataframe.df",\
                                                         "dataframe_matrix.npz")
    #print "## INFO ## Elements Read to generate Data Frame: {0}, matrix: {1}"\
    #                             .format(ELEMENTS_READ[0], ELEMENTS_READ[1])



    print "## INFO ## fin: {0}".format(datetime.datetime.now())
