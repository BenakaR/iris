import cv2
import numpy as np
import os

def knn_match(file_name: str) -> dict:
    image_files = [f for f in os.listdir(os.getcwd() + '/static/iris_data') ]
    match_data = {}
    print(len(image_files))
    for i in range(len(image_files)):
        file1 = image_files[i]
        try:
            similarity = flann_knn(file_name, file1)
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

    matches = flann.knnMatch(desc_1, desc_2, k=3)

    good_points = []

    for m, n, o in matches:
        if m.distance < 0.91*n.distance:
            good_points.append(m)
        elif n.distance < 0.91*o.distance:
            good_points.append(n)

    # Define how similar they are
    number_keypoints = 0
    if len(kp_1) <= len(kp_2):
        number_keypoints = len(kp_1)
    else:
        number_keypoints = len(kp_2)


    print("Keypoints 1ST Image: " + str(len(kp_1)))
    print("Keypoints 2ND Image: " + str(len(kp_2)))
    print("GOOD Matches:", len(good_points))
    print("How good it's the match: ", result_percent := (len(good_points) / number_keypoints * 100))

    return result_percent    

    # result = cv2.drawMatches(original, kp_1, image_to_compare, kp_2, good_points, None)
    # cv2.imshow("result", cv2.resize(result, None, fx=0.4, fy=0.4))
    # cv2.imwrite("feature_matching.jpg", result)
    # cv2.imshow("Original", cv2.resize(original, None, fx=0.4, fy=0.4))
    # cv2.imshow("Duplicate", cv2.resize(image_to_compare, None, fx=0.4, fy=0.4))
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()