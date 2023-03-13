import os 
from constants import *

class CervicalCancerContentReader():
  def __init__(self, data_dir, image_extension, data_extension="", sub_folder= ""):
    self.data_dir = data_dir 
    self.sub_folder = sub_folder
    self.image_extension = image_extension
    self.data_extension = data_extension
        
  def get_categories(self):
    return os.listdir(self.data_dir)

  def get_content_per_category(self, category):
    base_path = "{}/{}/{}/{}".format(self.data_dir, category, category, self.sub_folder)
    file_paths = os.listdir(base_path)
    image_paths = ["{}/{}".format(base_path, file_path) for file_path in file_paths if file_path.split(".")[-1] == self.image_extension]
    data_path = [file_path for file_path in file_paths if file_path.split(".")[-1] == self.data_extension]
    return (image_paths, data_path)

  def read(self):
    categories = self.get_categories()
    categories_content = {}
    
    for category in categories:
      (image_paths, data_path) = self.get_content_per_category(category)
      categories_content[category] = {IMAGE_PATH_KEY: image_paths, DATA_PATH_KEY: data_path}
    
    return categories_content
  

