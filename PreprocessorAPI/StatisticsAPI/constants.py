from backend.Storage import * 

database = DB()

PYTHON_NAME= "python3"
SERVER_PORT = "server_port"
SERVER_PASSWORD = "server_password"
EXECUTE_PYTHON_CMD = "{PYTHON_VERSION} {LOCATION}"

GUI_TITLE = "Plot and Image Viewer"
EVENT_NAME = "button_press_event"
EPSILON_Y = 0.01
PASSWORD = SERVER_PASSWORD
CP_FILE = "sshpass -p '{PASSWORD}' scp -P {PORT} -o 'StrictHostKeyChecking=no' -r {LOCAL_PATH} {SERVER_URL}:{REMOTE_PATH}"
CP_FILE_TO_LOCAL = "sshpass -p '{PASSWORD}' scp -P {PORT} -o 'StrictHostKeyChecking=no' -r {URL}:{PATH_REMOTE} {PATH_LOCAL}"
EXECUTE_CMD = "sshpass -p '{PASSWORD}' ssh -p {PORT} {SERVER_URL} {COMMAND}"
INPUT_URL = "Input URL"
INPUT_FILE_COLAB = "Input File to Copy"
BUTTON_BASH_EXECUTE = "Execute Bash Script In Colab"
BUTTON_PYTHON_EXECUTE = "Execute Python Script In Colab"
START_INDEX = "1.0"
BUTTON_COPY_FILE = "Copy File"
DST_PATH = "/content/{}"
BUTTON_COPY_FOLDER = "Copy Folder"
METADATA_LABEL = "label"
METADATA_IMAGE_PATH_KEY = "image_path"
METADATA_FEATURES_KEY = "features"
METADATA_DATA_KEY = "dataframe"
METADATA_FIGURE_KEY = "fig"
METADATA_AX_KEY = "ax"
COLUMN_AXIS = 1
TMP_FOLDER = "tmp"
STG_FILE = "stg.png"
LOAD_STG_FILE = "load.png"
BASH_RM_FILE = "rm -rf ./{FOLDER}/{FILE}"
BUTTON_CLICK_FLAG = 1
DATABASE_PATH = "./database/database.json"
PLOT_TYPE = "plot_type"
DATABASE_DATAFRAME_PATH_KEY = "dataframe_path"
DATABASE_LABEL_KEY = "current_label"
DATABASE_FEATURES_KEY = "features"
DATABASE_CLASS_FIELD_NAME = "class_field"
DATABASE_PATH_FIELD_NAME = "image_path_field"
DATABASE_URL_KEY = "server_url"
DATABASE_PATH_SRC = "path_src"
DATABASE_PATH_DST = "path_dst"

DATABASE_FLAG_KEY = "flag"
FEATURES = "features"
CLASS = "class"
IMAGE_PATH = "path"
LABELS_INFO = "labels_information"
PLOT_INFO = "plot_info"
LOF_PCA = "lof_pca"
LOF_TSNET = "lof_tsnet"
BOXPLOT = "boxplot"
SUPPORTED_PLOT_TYPES = [BOXPLOT, LOF_PCA] ## Add support for LOF_TSNET
SET_FEATURES = [DATABASE_FLAG_KEY, FEATURES, CLASS, IMAGE_PATH]
TMP_STORAGE = "tmp/{}"
DF_OUTLIERS_TMP = "df_outliers.csv"
TYPE = "type"
INDEXES = "indexes"
LOF_TMP_DF = TMP_STORAGE.format("lof.csv")