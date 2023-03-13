import os
import zipfile
from multiprocessing import Pool, cpu_count
import time

class DownloadDataset():
  def __init__(self, dataset_name, kaggle_key, dst_folder):
    self.create_folder = "mkdir {}".format(dst_folder)

    materialize_key = "echo '" + kaggle_key + "'" + ' > "kaggle.json"'
    export_kaggle = "export KAGGLE_CONFIG_DIR=$PWD"
    download_dataset = "kaggle datasets download -d {}".format(dataset_name)
    self.download_data_script = """
    {}
    {}
    {}
    """.format(materialize_key, export_kaggle, download_dataset)

    zip_path = "{}.zip".format(dataset_name.split("/")[-1])
    self.unzip_script = "unzip {} -d {}".format(zip_path, dst_folder)

  def download(self):
    self.run(self.download_data_script)
    self.run(self.create_folder)
    self.run(self.unzip_script)

  def run(self, cmd):
    print("Running... \n{}".format(cmd))
    os.system(cmd)


def measure_time(function, args=None):
  start = time.perf_counter()
  if args == None:
    function()
  else:
    function(args)
  end = time.perf_counter()
  elapsed_time = end - start
  print(f"Elapsed time: {elapsed_time} seconds")
