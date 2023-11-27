import cv2
import numpy as np
import os


# Saves a cropped image of all traffic barrels in the image
def extract_cropped_traffic_barrel(img_path):
    # Reads in the image and initializes the output_image
    input_image = cv2.imread(img_path)
    output_image = input_image

    # Converts the image to HSV color space
    hsv_image = cv2.cvtColor(input_image, cv2.COLOR_BGR2HSV)

    # Defines the lower and upper bounds for red-orange
    lower_orange = np.array([0, 100, 100])
    upper_orange = np.array([25, 255, 255])

    # Creates a mask for red-orange colors
    mask_orange = cv2.inRange(hsv_image, lower_orange, upper_orange)

    # Creates the kernel
    kernel = np.ones((5, 5), np.uint8)

    # Smooths the image
    thresh_smooth = cv2.erode(mask_orange, kernel)
    thresh_smooth = cv2.dilate(thresh_smooth, kernel)
    thresh_smooth = cv2.blur(thresh_smooth, (2, 2))

    # Finds the contours in the image
    contours, hierarchy = cv2.findContours(thresh_smooth, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

    # Filters out small contours
    large_contours = []
    height, width, _ = input_image.shape
    for each in contours:
        if cv2.contourArea(each) > height * width / 500:
            large_contours.append(each)

    # Returns a list of cropped, stacked contours
    return crop_stacked_contours(large_contours, output_image)


# Finds 3 contours that are stacked and returns the cropped images of these contour groups
def crop_stacked_contours(contour_list, image):
    # List of cropped images
    cropped_images = []

    for i in range(len(contour_list)):
        # List of contours that are stacked with i (Including that contour)
        stacked_contours = [contour_list[i]]

        # Finding the center x value for i
        m = cv2.moments(contour_list[i])
        if m["m00"] != 0:
            i_x = int(m["m10"] / m["m00"])

        # Goes through each contour and adds every contour stacked with the contour at i to stacked_contours
        for j in range(i + 1, len(contour_list)):
            # Finding the center x value for j
            m = cv2.moments(contour_list[j])
            if m["m00"] != 0:
                j_x = int(m["m10"] / m["m00"])

            # Checks to see if contours are stacked
            if abs(i_x - j_x) < 50:
                stacked_contours.append(contour_list[j])

        # Assumed to be a traffic barrel if there are 3 stacked contours
        if len(stacked_contours) == 3:
            # Concatenate all contours
            cnts = np.concatenate(stacked_contours)

            # Determines the bounding rectangle
            x, y, w, h = cv2.boundingRect(cnts)

            extend_x = int(w * 0.15)
            extend_y = int(h * 0.15)

            y1 = y - extend_y if y - extend_y >= 0 else 0
            x1 = x - extend_x if x - extend_x >= 0 else 0
            y2 = y + h - 1 + extend_y
            x2 = x + w - 1 + extend_x

            # cv2.rectangle(image, (x1, y1), (x2, y2), 255, 2)

            # Adds a cropped image to cropped_images
            cropped_images.append(image[y1:y2, x1:x2])

    return cropped_images


directory = "C:\\Users\\rynom\\PycharmProjects\\trafficBarrelImageExtraction\\images"
for filename in os.listdir(directory):
    if filename.endswith(".jpg") or filename.endswith(".png"):
        cropped_images = extract_cropped_traffic_barrel(directory + "\\" + filename)
        for i in range(len(cropped_images)):
            split_filename = filename.split(".")
            cv2.imwrite("output\\" + split_filename[0] + "_" + str(i) + "." + split_filename[1], cropped_images[i])
