import pandas as pd
from ini import * 
from constants import * 

class ExperimentDataReader():
    def read(self):
        path_image = database.readContent(DATABASE_DATAFRAME_PATH_KEY)
        label = database.readContent(DATABASE_LABEL_KEY)
        features = database.readContent(DATABASE_FEATURES_KEY)
        class_field_name = database.readContent(DATABASE_CLASS_FIELD_NAME)
        path_field_name = database.readContent(DATABASE_PATH_FIELD_NAME)

        df = pd.read_csv(path_image)
        df_filter = df[df[class_field_name] == label]
        df_raw = df_filter[[path_field_name] + features].reset_index()
        df_norm = self.mim_max_normalization(df_raw, features)
        metadata = {
            METADATA_DATA_KEY: df_norm,
            METADATA_FEATURES_KEY: features,
            METADATA_IMAGE_PATH_KEY: path_field_name,
            METADATA_LABEL: label
        }
        return metadata

    def mim_max_normalization(self, df_raw, features):
        for feature in features:
            df = df_raw[feature]
            max = df.max()
            min = df.min()
            max_distance = max - min
            df_raw[feature] = (df_raw[feature].astype(float) - min) / max_distance
        return df_raw
