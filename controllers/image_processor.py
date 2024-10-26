import cv2
import numpy as np
from models.db import VegetationDatabase


class ImageProcessor():
    def __init__(self, input_image):
        self.db = VegetationDatabase()
        self.input_image = input_image
        self.original_image = cv2.imread(self.input_image)

    def enhance_green_vegetation(self, output_path=None):
        # Load the image
        img = cv2.imread(self.input_image)

        # Convert to HSV color space
        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

        # Define range for green color in HSV
        lower_green = np.array([40, 20, 20])
        upper_green = np.array([80, 255, 255])

        # Create a mask to isolate green vegetation
        mask = cv2.inRange(hsv, lower_green, upper_green)

        # Create a green enhancement layer
        green_enhance = np.zeros_like(img)
        green_enhance[:, :, 1] = mask  # Set green channel to the mask

        # Blend the green enhancement with the original image
        alpha = 0.3
        enhanced = cv2.addWeighted(img, 1, green_enhance, alpha, 0)

        # Increase overall brightness and contrast
        brightness = 30
        contrast = 1.3
        enhanced = cv2.addWeighted(enhanced, contrast, np.zeros_like(enhanced), 0, brightness)

        # Optional: Apply a slight sharpening filter
        kernel = np.array([[-1, -1, -1], [-1, 9, -1], [-1, -1, -1]])
        enhanced = cv2.filter2D(enhanced, -1, kernel)

        # Save the result
        if output_path != None:
            cv2.imwrite(output_path, enhanced)

        return enhanced

    def detect_and_analyze_vegetation(self, image, image_path):
        # Convert to HSV color space
        hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

        # Define range of green color in HSV
        lower_green = np.array([30, 40, 40])
        upper_green = np.array([90, 255, 255])

        # Threshold the HSV image to get only green colors
        mask = cv2.inRange(hsv, lower_green, upper_green)

        # Find contours in the mask
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        # Prepare data storage
        vegetation_data = []

        # Analyze each contour
        for i, contour in enumerate(contours):
            # Calculate area
            area = cv2.contourArea(contour)

            # Filter out very small areas (adjust as needed)
            if area > 100:
                # Get bounding rectangle
                x, y, w, h = cv2.boundingRect(contour)

                # Calculate centroid
                m = cv2.moments(contour)
                if m["m00"] != 0:
                    cx = int(m["m10"] / m["m00"])
                    cy = int(m["m01"] / m["m00"])
                else:
                    cx, cy = x + w // 2, y + h // 2

                # Store data
                vegetation_data.append({
                    "id": i,
                    "area": area,
                    "bounding_box": (x, y, w, h),
                    "centroid": (cx, cy)
                })

                # Draw contour and centroid on the image (for visualization)
                cv2.drawContours(image, [contour], 0, (0, 255, 0), 2)
                cv2.circle(image, (cx, cy), 5, (0, 0, 255), -1)

                # Store vegetation patch data in each loop
                if vegetation_data != []:
                    self.db.store_scan_data(image_path, vegetation_data)
                else:
                    pass

        # Store image data after loop is done
        if vegetation_data != []:
            print("Storing image data...")
            self.db.store_image_data(image_path, vegetation_data)
            self.db.close()
        else:
            print("No patches found...")
        return image, vegetation_data

"""
    def get_model_training_data(self):
        db = VegetationDatabase()
        try:
            features, targets = db.get_training_data()
            return features, targets
        finally:
            db.close()
            """


