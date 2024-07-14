import cv2
import numpy as np
import os

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

def knn_match(file_name: str) -> dict:
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
