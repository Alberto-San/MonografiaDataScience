import cv2
from constants import *
import scipy.ndimage as ndi
import numpy as np
from scipy.stats import moment
import skimage.measure
import logging

logger = logging.getLogger()

class CalculateImageClasicalFeatures():
    '''
        @ Is only support to work with color_space BGR and GRAY
    '''
    def __init__(self, color_space):
        self.color_space = color_space

    def average_contrast(self, image_bgr):
        image_y_cr_cb = cv2.cvtColor(image_bgr, cv2.COLOR_BGR2YCrCb)
        luminance = image_y_cr_cb[:, :, LUMINANCE_COMPONENT]
        average = luminance.mean()
        return average
    
    def standard_deviation(self, image_component):
        std = image_component.std()
        return std
    
    def average_intensity(self, image_component):
        average = image_component.mean()
        return average
    
    def smoothness(self, image_component):
        #https://stackoverflow.com/questions/24671901/does-there-exist-a-way-to-directly-figure-out-the-smoothness-of-a-digital-imag
        im_normalize = image_component.astype(float) / 255.0
        im_laplace_filter = ndi.filters.laplace(im_normalize)
        im_abs = np.absolute(im_laplace_filter)
        average = np.average(im_abs)
        return average

    def uniformity(self, image_component):
        #https://stackoverflow.com/questions/46444286/measure-of-uniformity-homogeniy-in-an-image-c-opencv
        im_normalize = image_component.astype(float) / 255.0
        kernel_size = (11, 11)
        sigma = 2
        gaussian_blur = lambda im_normalize: cv2.GaussianBlur(im_normalize, kernel_size, sigma)
        gaussian_blur_cicle = lambda im_normalize, times=1: gaussian_blur(im_normalize) if times == 1 else gaussian_blur_cicle(gaussian_blur(im_normalize), times=times - 1)
        blur_non = gaussian_blur_cicle(im_normalize, 11)
        last_blur_non = gaussian_blur(blur_non)
        diff = last_blur_non - blur_non
        ssd_blur_non = np.sum(diff**2)
        return ssd_blur_non
    
    def third_moment(self, image_component):
        array = image_component.reshape(-1)
        moment_ = moment(array, moment = 3)
        return moment_
    
    def median(self, image_component):
        array = image_component.reshape(-1)
        return np.median(array)

    def entropy(self, image_component):
        entropy = skimage.measure.shannon_entropy(image_component)
        return entropy
    
    def calculate_features(self, im):
        '''
        @ im must be an opencv object/ numpy that is in the scale (0, 255)
        '''
        try:
            if self.color_space == "gray" and len(im.shape) > 2:
                raise Exception("gray space was selected, but you are trying to get features from a color image")
            
            elif self.color_space == "bgr" and len(im.shape) < 3:
                raise Exception("bgr space was selected, but you are trying to get features from a gray image") 
            else:
                features = [
                        self.average_intensity,
                        self.smoothness,
                        self.uniformity,
                        self.third_moment,
                        self.entropy,
                        self.standard_deviation,
                        self.median
                    ]
                feature_vector = []
                if self.color_space == "bgr":
                    components = 3
                    for idx_component in range(components):
                        im_component = im[:, :, idx_component]
                        #print("im_component is: {}".format(im_component.shape))
                        [feature_vector.append(feature(im_component)) for feature in features]

                    feature_vector.append(self.average_contrast(im))
                else:
                    [feature_vector.append(feature(im)) for feature in features]

        except Exception as e:
            logger.error("Error occur while trying to execute `CalculateFeatures('{}').calculate_features(im)`".format(self.color_space))
            print("im shape is: {}".format(im.shape))
            print(e)
            logger.error(e)

        return feature_vector