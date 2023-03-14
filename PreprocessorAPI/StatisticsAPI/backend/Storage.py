import json
import os

PLOT_TYPE = "plot_type"
DATABASE_DATAFRAME_PATH_KEY = "dataframe_path"
DATABASE_LABEL_KEY = "current_label"
DATABASE_FEATURES_KEY = "features"
DATABASE_CLASS_FIELD_NAME = "class_field"
DATABASE_PATH_FIELD_NAME = "image_path_field"
DATABASE_URL_KEY = "server_url"
DB_NAME = "db.json"
DB_PATH = "MonografiaDataScience/PreprocessorAPI/StatisticsAPI/database/{}".format(DB_NAME)
WRITE_MODE = "w"
READ_MODE = "r"
DATABASE_FLAG_KEY = "flag"
SERVER_PORT = "server_port"
SERVER_PASSWORD = "server_password"
DATABASE_PATH_DST = "path_dst"

class DB():
    def __init__(self):
        folder = os.listdir("MonografiaDataScience/PreprocessorAPI/StatisticsAPI/database")
        folder = [elem for elem in folder if elem.split(".")[-1] == "json"]
        if DB_NAME not in folder:
            self.initStateDb()

    def readDB(self):
        with open(DB_PATH, READ_MODE) as fp:
            database = json.load(fp)
        fp.close()
        return database

    def writeDB(self, database):
        with open(DB_PATH, WRITE_MODE) as fp:
            json.dump(database, fp)
        fp.close()

    def initStateDb(self):
        database = {
            DATABASE_FEATURES_KEY: [],
            DATABASE_DATAFRAME_PATH_KEY: "",
            DATABASE_LABEL_KEY: "",
            DATABASE_CLASS_FIELD_NAME: "class",
            DATABASE_PATH_FIELD_NAME: "image_path",
            PLOT_TYPE: "",
            DATABASE_URL_KEY: "",
            DATABASE_FLAG_KEY: "",
            SERVER_PORT: "22",
            SERVER_PASSWORD: "",
            DATABASE_PATH_DST: ""
        }
        self.writeDB(database)
    
    def writeValueDb(self, key, value):
        database = self.readDB()
        if key == "object_path":
            database[key].append(value)
        else:
            database[key] = value

        self.writeDB(database)

    def readContent(self, key):
        database = self.readDB()
        return database[key]
    
