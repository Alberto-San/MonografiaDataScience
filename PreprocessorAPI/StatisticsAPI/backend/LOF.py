from ini import *
from constants import *
from backend.ExperimentDataReader import ExperimentDataReader
from sklearn.neighbors import LocalOutlierFactor
import numpy as np
from sklearn.decomposition import PCA
from matplotlib.figure import Figure
import pandas as pd
from joblib import dump, load

WINDOW_SIZE = (5, 4)

class LOF():
    def __init__(self):
        None 
    
    def predict_data_once_model(self):
        # https://scikit-learn.org/stable/modules/generated/sklearn.neighbors.LocalOutlierFactor.html
        clf = load('MonografiaDataScience/tmp/lof.joblib') 
        None

    def process_data(self, data_numeric_features, k=5):
        lof_processor = LocalOutlierFactor(
            n_neighbors=k, 
            algorithm="auto", 
            contamination=0.05, 
            metric="euclidean", 
            n_jobs=-1
        )
        processed_data = lof_processor.fit_predict(data_numeric_features)
        criteria = lof_processor.negative_outlier_factor_
        label = database.readContent(DATABASE_LABEL_KEY)
        dump(lof_processor, 'MonografiaDataScience/tmp/lof_{}.joblib'.format(label)) 
        print("lof model for label {} was saved to {}".format(label, "MonografiaDataScience/tmp/lof_{}.joblib".format(label)))
        return (processed_data, criteria)

    def get_index(self, processed_data, ground_truth, condition="eq"):
        indexes = np.where(processed_data == ground_truth) if condition == "eq" else np.where(processed_data != ground_truth)
        array_index = np.asarray(indexes)
        stack_index = np.hstack(array_index)
        return stack_index, indexes

    def outlier_analysis(self):
        metadata = ExperimentDataReader().read()
        self.metadata = metadata
        data_raw = metadata[METADATA_DATA_KEY]
        features = metadata[METADATA_FEATURES_KEY]
        data_numeric_features = data_raw[features]

        (processed_data, _) = self.process_data(data_numeric_features)

        ground_truth = np.ones(len(data_numeric_features), dtype=int)
        stack_index, indexes = self.get_index(processed_data, ground_truth)
        stack_index_outliers, _ = self.get_index(processed_data, ground_truth, "neq")

        self.metadata[INDEXES] = indexes

        self.data_outliers = data_raw.iloc[stack_index_outliers]
        self.data_outliers[TYPE] = "outlier"
        self.data_typical = data_raw.iloc[stack_index]
        self.data_typical[TYPE] = "normal"

    def get_data(self):
        self.outlier_analysis()
        pca = PCA()
        path_field = database.readContent(DATABASE_PATH_FIELD_NAME)
        features = database.readContent(DATABASE_FEATURES_KEY)
        numeric_data = [
                self.data_outliers[features], 
                self.data_typical[features]
            ]
        X = pd.concat(numeric_data, ignore_index=True)
        Xt = pca.fit_transform(X)
        columns = ["Component_{}".format(index) for index in range(Xt.shape[1])]
        Xt_df = pd.DataFrame(Xt, columns=columns)
        Xt_df[TYPE] = pd.concat([self.data_outliers[TYPE], self.data_typical[TYPE]], ignore_index=True)
        Xt_df[path_field] = pd.concat([self.data_outliers[path_field], self.data_typical[path_field]], ignore_index=True)
        Xt_df.to_csv(LOF_TMP_DF, index=False)

    def process_to_plot(self, df):
        path_field = database.readContent(DATABASE_PATH_FIELD_NAME)
        descriptors = [TYPE, path_field]
        numeric = df.drop(descriptors, axis=1).to_numpy()
        x0 = numeric[:, 0]
        x1 = numeric[:, 1]
        return x0, x1
    
    def get_plot(self):
        self.get_data()

        df = pd.read_csv(LOF_TMP_DF)
        df_outliers = df[df[TYPE] == "outlier"]
        df_normal = df[df[TYPE] == "normal"]
        x0_n, x1_n = self.process_to_plot(df_normal)
        x0_o, x1_o = self.process_to_plot(df_outliers)

        fig = Figure(figsize=WINDOW_SIZE, dpi=100)
        ax = fig.add_subplot(111)
        ax.plot(x0_n, x1_n, ".", c="blue")
        ax.plot(x0_o, x1_o, ".", c="red")
        return fig, ax

    def get_outliers(self):
        path_field = database.readContent(DATABASE_PATH_FIELD_NAME)
        df_lof_pca = pd.read_csv(LOF_TMP_DF)
        df_outliers_path = df_lof_pca[df_lof_pca[TYPE] == "outlier"][path_field]
        df_outliers_path.to_csv(TMP_STORAGE.format(DF_OUTLIERS_TMP), index=False)
