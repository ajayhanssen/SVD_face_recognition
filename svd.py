import cv2
import numpy as np
import os


class Match():
    def __init__(self, index=None, score=None):
        self.index = index
        self.score = score

class SVD_Object():
    """
    Class to perform Singular-value-decomposition on images
    """
    def __init__(self):
        self.images = None
        self.U = None
        self.S = None
        self.V = None
        self.meantrain = None
        self.status = {'trained': False} # Dictionary for information, maybe more added later on

    def train(self, directory : str ="./source_images/") -> None:
        """
        Function to train SVD-Model based on images in ./source_images/ directory

        Inputs:
            directory (str) : Folder containing  images to train the model on
        Returns:
            None
        """


        #-------------------------------1--------------------------------#
        #-------------------READ IMAGES FROM DIRECTORY-------------------#
        
        trainfiles = os.listdir(directory)                                  #-----------List of all the files in the directory
        images = []                                                         #-----------Empty List to store the images

        for file in trainfiles:                                             #-----------Iterating over all the files in the directory
            img = cv2.imread(directory + file, cv2.IMREAD_GRAYSCALE)
            images.append(img.flatten())                                    #-----------Collapsing the image into a 1D array and appending to the list of images
        
        images = np.array(images)                                           #-----------Converting the list of images to a numpy array
        
        
        #-------------------------------2--------------------------------#
        #-------------------PREPROCESSING OF IMAGES----------------------#
        
        meantrain = np.mean(images)                                         #-----------Calculating the mean of the images
        images = images - meantrain                                         #-----------Subtracting the mean from the images
        images = images.T                                                   #-----------Transposing the matrix from == to || (said like a professional)

        
        #-------------------------------3--------------------------------#
        #------------------------------SVD-------------------------------#
        
        self.U, self.S, self.V = np.linalg.svd(images, full_matrices=False) #-----------Performing SVD on the images (full_matrices=false makes for better performance apparently)
        self.meantrain = meantrain
        self.images = images
        self.status['trained'] = True                                       #-----------Setting the status of the model to trained
        return


    def predict(self, pred_image) -> Match:
        """
        Function to predict the image based on the trained model

        Inputs:
            pred_image (np.array) : Image to predict (ret,frame = cap.read() --> frame already np-array)
        Returns:
            Object (Match) : contains index and score of the matched image
        """


        #-------------------------------1--------------------------------#
        #-------------------PREPROCESSING OF IMAGES----------------------#

        pred_image = cv2.cvtColor(pred_image, cv2.COLOR_BGR2GRAY)           #-----------Converting the image to grayscale
        pred_image = pred_image.reshape(1, -1)                              #-----------Collapsing the image into a 1D array again


        #-------------------------------2--------------------------------#
        #-------------------PREDICTING THE IMAGE-------------------------#

        pred_image = pred_image - self.meantrain                            #-----------Subtracting the mean from the image
        pred_image = pred_image.T                                           #-----------Transposing the array from -- to | (yes)

        projected_image = np.dot(self.U.T, pred_image)                      #-----------Projecting the image onto the U matrix
        projected_training_images = np.dot(self.U.T, self.images)           #-----------Projecting the training images onto the U matrix

        distances = np.linalg.norm(projected_training_images - projected_image, axis=0) #-----------Calculating distance between test image and projected training images
        match_index = np.argmin(distances)                                  #-----------Finding the index of the image with the least distance
        match_score = distances[match_index]                                #-----------Finding the distance of the matched image

        return Match(match_index, match_score)                              #-----------Returning the match object

    def find_source_image(self, match: Match, directory : str ="./source_images/") -> str:
        """
        Function to find the source image based on the match object

        Inputs:
            match (Match) : Object containing index and score of the matched image
            directory (str) : Folder containing images to train the model on
        Returns:
            name (str) : Name of the matched image
        """
        trainfiles = os.listdir(directory)                                  #-----------List of all the files in the directory
        return trainfiles[match.index]                                      #-----------Returning the name of the matched image


if __name__ == "__main__":
    SVD = SVD_Object()
    SVD.train("./source_images/")
    result = SVD.predict(cv2.imread("./source_images/1.jpg"))

    print(result.index, result.score)
