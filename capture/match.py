import cv2
import numpy as np
import os
from scipy.spatial.distance import hamming

# def extract_features(image_path: str) -> np.ndarray:
#     # Read the image
#     image = cv2.imread(image_path)

#     # Convert to grayscale
#     gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

#     # Detect the iris boundary using Circular Hough Transform
#     circles = cv2.HoughCircles(gray, cv2.HOUGH_GRADIENT, 1, 200, param1=100, param2=30, minRadius=50, maxRadius=150)
#     x, y, r = circles[0]

#     # Extract the iris region
#     iris_region = gray[y-r:y+r, x-r:x+r]

#     # Normalize the iris region
#     iris_region = cv2.normalize(iris_region, None, 0, 255, cv2.NORM_MINMAX)

#     # Extract LBP features
#     lbp_features = local_binary_pattern(iris_region, 8, 3, 'uniform')

#     return lbp_features

def match_iris(file_name: str) -> dict:
    image_files = [f for f in os.listdir(os.getcwd() + '/static/iris_data') ]
    match_data = {}
    print(len(image_files))
    for i in range(len(image_files)):
        file1 = image_files[i]
        try:
            similarity = eye_similarity(file_name, file1)
        except:
            similarity = 0
        match_data.update({file1 : similarity})
        print(i)
    max = 0
    max_file = ''
    for file in match_data:
        if match_data[file] > max:
            max = match_data[file]
            max_file = file
    return [max_file, max]

def flann_knn(file1: str,file2: str) -> float:
    path = os.getcwd() + '\static\%s' % (file1)
    image_read = cv2.imread(path)
    original = image_read

    path = os.getcwd() + '\static\iris_data\%s' % (file2)
    image_read = cv2.imread(path)
    image_to_compare = image_read

    if original.shape == image_to_compare.shape:
        print("The images have same size and channels")
        difference = cv2.subtract(original, image_to_compare)
        b, g, r = cv2.split(difference)
        if cv2.countNonZero(b) == 0 and cv2.countNonZero(g) == 0 and cv2.countNonZero(r) == 0:
            print("The images are completely Equal")
            return 100.0
        else:
            print("The images are NOT equal")

    # 2) Check for similarities between the 2 images
    sift = cv2.xfeatures2d.SIFT_create()
    kp_1, desc_1 = sift.detectAndCompute(original, None)
    kp_2, desc_2 = sift.detectAndCompute(image_to_compare, None)

    index_params = dict(algorithm=0, trees=5)
    search_params = dict()
    flann = cv2.FlannBasedMatcher(index_params, search_params)

    matches = flann.knnMatch(desc_1, desc_2, k=2)

    good_points = []

    for m, n, o in matches:
        if m.distance < 0.7*n.distance:
            good_points.append(m)

    # Define how similar they are
    number_keypoints = 0

    number_keypoints = len(kp_1)



    print("Keypoints 1ST Image: " + str(len(kp_1)))
    print("Keypoints 2ND Image: " + str(len(kp_2)))
    print("GOOD Matches:", len(good_points))
    print("How good it's the match: ", result_percent := (len(good_points) / number_keypoints * 100))

    return result_percent    

def eye_similarity(file1: str, file2: str) -> float:

    # Read the images
    image1_path = os.getcwd() + '\static\%s' % (file1)
    image2_path = os.getcwd() + '\static\iris_data\%s' % (file2)
    image1 = cv2.imread(image1_path)
    image2 = cv2.imread(image2_path)

    # Convert images to grayscale
    gray1 = cv2.cvtColor(image1, cv2.COLOR_BGR2GRAY)
    gray2 = cv2.cvtColor(image2, cv2.COLOR_BGR2GRAY)

    # Calculate the histogram of both images
    hist1 = cv2.calcHist([gray1], [0], None, [256], [0, 256])
    hist2 = cv2.calcHist([gray2], [0], None, [256], [0, 256])

    # Calculate the correlation coefficient between the two histograms
    corr_coef = cv2.compareHist(hist1, hist2, cv2.HISTCMP_CORREL)

    # Calculate the similarity score
    similarity_score = corr_coef * 100

    return similarity_score


def process_iris_image(image_path):
    # Step 1: Load the image
    img = cv2.imread(image_path)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Step 2: Detect the iris
    # Note: This is a simplified approach. For more accurate results,
    # consider using specialized iris segmentation algorithms.
    circles = cv2.HoughCircles(gray, cv2.HOUGH_GRADIENT, dp=1, minDist=50,
                               param1=50, param2=30, minRadius=20, maxRadius=100)

    if circles is not None:
        circles = np.uint16(np.around(circles))
        iris_circle = circles[0][0]  # Assume the first detected circle is the iris
        
        # Step 3: Create a mask for the iris
        mask = np.zeros(gray.shape, dtype=np.uint8)
        cv2.circle(mask, (iris_circle[0], iris_circle[1]), iris_circle[2], 255, -1)
        
        # Step 4: Apply the mask to isolate the iris
        iris = cv2.bitwise_and(gray, gray, mask=mask)
        
        # Step 5: Initialize SIFT detector
        sift = cv2.SIFT_create()
        
        # Step 6: Detect keypoints and compute descriptors
        keypoints, descriptors = sift.detectAndCompute(iris, None)
        
        # Step 7: Convert descriptors to a binary representation
        # Note: This step is optional and depends on your specific requirements
        binary_descriptors = (descriptors > np.mean(descriptors)).astype(int)
        
        return binary_descriptors
    else:
        print("No iris detected in the image.")
        return None


def compare_iris_features(image_path1, image_path2):
    """
    Compare two sets of binary iris features and return a similarity score.
    
    Args:
    features1, features2 (numpy.ndarray): Binary feature arrays to compare
    
    Returns:
    float: Similarity score between 0 and 1, where 1 is a perfect match
    """
    path = os.getcwd() + '\static\%s' % (image_path1)
    features1 = process_iris_image(path)

    path = os.getcwd() + '\static\iris_data\%s' % (image_path2)
    features2 = process_iris_image(path)

    if features1.shape != features2.shape:
        raise ValueError("Feature arrays must have the same shape")
    
    # Calculate the average Hamming distance across all feature vectors
    distances = [hamming(f1, f2) for f1, f2 in zip(features1, features2)]
    avg_distance = np.mean(distances)
    
    # Convert distance to similarity score (0 to 1)
    similarity = 1 - avg_distance
    
    return similarity



