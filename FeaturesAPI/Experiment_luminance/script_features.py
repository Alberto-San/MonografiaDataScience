import cv2
import pandas as pd
import cv2
from scipy.stats import moment
from CervicalCancerContentReader import *
from CalculateImageClasicalFeatures import *
from constants import *
import multiprocessing

sub_folder = "CROPPED"
image_extension = "bmp"
data_extension = "dat"
dataset_output_path = input("Input the folder that contains sipakmed data: \n")
size = (220, 220)

categories_content = CervicalCancerContentReader(
                        dataset_output_path,
                        image_extension,
                        data_extension,
                        sub_folder
                    ).read()

labels = list(categories_content.keys())


def multiprocessing_logic(items, function):
    num_processes = multiprocessing.cpu_count()
    pool = multiprocessing.Pool(num_processes)
    output_list = pool.map(function, items)
    return output_list

def get_luminance_component(path):
    print("path: {}".format(path))
    image_bgr = cv2.imread(path)
    image_y_cr_cb = cv2.cvtColor(image_bgr, cv2.COLOR_BGR2YCrCb)
    luminance = image_y_cr_cb[:, :, LUMINANCE_COMPONENT]
    luminance = cv2.resize(luminance, size, interpolation=cv2.INTER_LINEAR)
    return luminance

def get_color_component(path):
    print("path: {}".format(path))
    image_bgr = cv2.imread(path)
    color_component = cv2.resize(image_bgr, size, interpolation=cv2.INTER_LINEAR)
    return color_component

def get_descriptor(args):
    index, label, image_paths, image_component, hanlder = args
    return [label, image_paths[index]] + hanlder.calculate_features(image_component)

def calculate_features_label(label, categories_content):
    hanlder = CalculateImageClasicalFeatures("gray")
    image_paths = categories_content[label][IMAGE_PATH_KEY]
    num_processes = multiprocessing.cpu_count() - 1
    pool = multiprocessing.Pool(num_processes) #[get_luminance_component(path) for path in image_paths]
    print("Reading Images")
    im_list = pool.map(get_luminance_component, image_paths) #pool.map(get_luminance_component, image_paths)
    function_args = [(index, label, image_paths, im_list[index], hanlder) for index in range(len(im_list))]
    print("Getting Descriptors")
    features = pool.map(get_descriptor, function_args) #multiprocessing_logic(items=function_args, function=get_descriptor)
    return features

accum_list = []
accum_labels = []
flag_define_labels = False
for label in labels:
    [accum_list.append(feature) for feature in calculate_features_label(label, categories_content)]

    if not(flag_define_labels):
        accum_labels = ["feature_{}".format(index) for index in range(len(accum_list[0])-2)]
        flag_define_labels = True
    

columns = [
    "class",
    "image_path"
    ] + accum_labels
df = pd.DataFrame(accum_list, columns=columns)

df.to_csv("./tmp/luminance_statistics.csv", index=False)