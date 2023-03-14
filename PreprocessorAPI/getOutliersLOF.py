# Dependencias
'''
constanst.py
LOF.py
 - ExperimentDataReader.py
tmp folder
'''
from ini import *
import pandas as pd
from backend.LOF import LOF
from constants import *
import os
import matplotlib.pyplot as plt
import logging

def map_function(function, list):
    return [function(elem) for elem in list]

def get_outliers(current_class):
    database.writeValueDb(DATABASE_LABEL_KEY, current_class)
    outliers_processor = LOF()
    fig, ax = outliers_processor.get_plot() # Internally, this saves a dataframe in path tmp/lof.csv
    plt.show()
    cp_command = "cp MonografiaDataScience/tmp/lof.csv MonografiaDataScience/tmp/lof_{}.csv".format(current_class)
    print("Outliers of {} is located at {}".format(current_class, "MonografiaDataScience/tmp/lof_{}.csv".format(current_class)))
    os.system(cp_command)

def filter_outliers(current_class):
    path = "MonografiaDataScience/tmp/lof_{}.csv".format(current_class)
    table_lof = pd.read_csv(path)
    table_lof_normal = table_lof[table_lof["type"] != "outlier"]
    table_lof_normal["class"] = current_class
    output_labels = ["image_path"]
    output_table = table_lof_normal[output_labels]
    return output_table

logger = logging.getLogger('my_logger')

# path_csv = "/home/daniel/Documents/Cursos/Especializacion/luminance_statistics.csv" #input("Input the path of csv features file: \n")
# class_field = input("Input the class field that contains the class that a register belongs to: \n")
# path_field = input("Input the path field that contains the information regarding to the path of the images: \n")

def run_outliers_analisis(path_csv, class_field, path_field):
    logger.debug("Reading Input Table...")
    features_table = pd.read_csv(path_csv)
    columns_table = features_table.columns

    non_numerical_features = [path_field, class_field]
    numerical_features = [feature for feature in columns_table if feature not in non_numerical_features]

    logger.debug("Reading Table Classes...")
    table_classes = features_table[class_field].drop_duplicates()
    classes = list(table_classes.values.reshape(-1))

    logger.debug("Writing information to local database..")
    # Saving information to current database. This is because the use modules share their status through the database
    database.writeValueDb(DATABASE_FEATURES_KEY, numerical_features)
    database.writeValueDb(DATABASE_CLASS_FIELD_NAME, class_field)
    database.writeValueDb(CLASS, class_field)
    database.writeValueDb(DATABASE_PATH_FIELD_NAME, path_field)


    logger.debug("Getting outlier data...")
    map_function(function=get_outliers, list=classes)

    logger.debug("Filtering outlier data...")
    data_without_outliers = map_function(function=filter_outliers, list=classes)
    table_without_outliers = pd.concat(data_without_outliers, axis=0)

    logger.debug("Removing outliers from original table...")
    original_data_without_outliers = pd.merge(features_table, table_without_outliers, on=path_field)
    original_data_without_outliers.to_csv("MonografiaDataScience/tmp/filtered_data.csv", index=False)
    print("Data Without Outliers is located at {}".format("MonografiaDataScience/tmp/filtered_data.csv"))
