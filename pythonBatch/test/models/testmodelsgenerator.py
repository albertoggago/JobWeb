import sys
import logging

sys.path.insert(0, "..")
sys.path.insert(0, "..")
from pyproj.models.modelsgenerator import ModelsGenerator


def test_error_file_config():
    models_generator = ModelsGenerator("config/configModelsxx.json", logging.DEBUG)
    assert models_generator

def test_generate_dataframe_error_path():
    models_generator = ModelsGenerator("config/configModels.json", logging.DEBUG)
    result = models_generator.generate_dataframe("data/", "dataframe.df")
    assert result

def test_generate_dataframe_without_matrix():
    models_generator = ModelsGenerator("config/configModels.json", logging.DEBUG)
    result = models_generator.generate_dataframe("data/", "dataframe.df")
    assert result

def test_generate_dataframe_with_matrix():
    models_generator = ModelsGenerator("config/configModels.json", logging.DEBUG)
    result = models_generator.generate_dataframe("data/", "dataframe.df",)
    assert result
