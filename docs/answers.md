# What did you learn after looking on our dataset?
The data is collected from four different surveillance cameras in parking lots. The data is collected based on some activity detection system, but it is affected by the illumination changes in the environment. Some images are captured at a different resolution, and one image is corrupted. The interesting parts, probably for the downstream task, are the activity in the scene and/or the free parking space. 

# How does you program work?
The implemented program focus on the cleaning files and naming structure first. This code utilizes a frame by frame comparison to identify the duplicates, this method reduces the number of combinations and retains the useful information. A suitable Gaussian blur radius is selected to smooth the images and reduce noise. Further thesholds are used to compute the similarity between them. Finally, duplicates are removed from the filtered list. 
# What values did you decide to use for input parameters and how did you find these values?
The parameters are found based on the random search method and parameter range is selected by analyzing the dataset quantitatively. 

| Parameter  |  Range |  selected value |  
|---|---|---|
| Gaussian kernel size  | 3-27  | 21  | 
|  Minimum contour area | 10-500  | 100  |  
|  Similarity threshold score | 500 - 2000  | 1000  |   

* Gaussian kernel size: This parameter decides the level of Gaussian filtering applied to smooth the image and filters out high fequency noise from the images. The kernel size should be selected such that filtering keeps useful information in the image while removing noise from it. I experimented with the range mentioned the table and found size of 21 to be suitable value.

* Minimum contour area: The computed contour list consists of lot of small contours which is probably noise of mimimal change between the frames. This parameter helps to remove contours with small area and the scores represent major differneces of the frames. I found this parameter by observing values setting a 0 to this parameter and vary only the kernel size. 

* Duplicate threshold score: The final score to represent the score is computed by sum of area of all contours. A pair of images are similar if they have a score near to 0. However, due to illumination changes an off
set of 1000 was found to be suitable. A large value does not mean images contain useful inforamtion due to the large illumintaion changes an upper threshold would be better but a single threshold did not result in a good filtering hence, only lower threshold is used.


# What you would suggest to implement to improve data collection of unique cases in future?

While Implementing the current script few ideas that came to me are listed as follows:

* Since the camera field of view seems to be fixed a image with only background information can be used to filter the interesting parts of the scene and this can be used for filtering the duplicates
* Current method relies on difference between two frames instead of this apporach, from each image features can be obtained to create a descriptors. A similarity score computed between the descriptors using distance metrics like cosine similarity. 
* Another apporach is to utilize the histogram of images to filter the ilumination and glare. A histogram bin-wise comparision can be applied to find the duplicates.
* Deep learning based method can be employed to identify objects in the scene and images without any interesting objects for the downstream task can be considered as duplicates. 
* Currently, comparison is done between two consecutive frames which can be extended by a sliding window method to retain relevant frames.
* Unsupervised or semi-supervised method can be used to cluster the data to effectively identify the duplicates. 
* A mask can be genreated to filter the illuminated areas of the images to compare the interesting information of the scenes.


# Any other comments about your solution?
Then method submitted is a starting point for identify the duplicates. The comparison method is not robust to illumination change, which results in frames that are not identified as duplicates. However, it does a good job in identify duplicates overall. 