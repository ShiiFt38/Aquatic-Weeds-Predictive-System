import ee
import geemap
import os
from dotenv import load_dotenv
from datetime import datetime

class Satellite:
    def __init__(self):
        # Initialize Earth Engine
        print("Initiating project...")
        # self.auth = ee.Authenticate()
        load_dotenv()
        self.PROJECT_ID = os.getenv("EarthEngine_Project")
        ee.Initialize(project=self.PROJECT_ID)
        print("Initiated!")

        # Define Hartbeespoort Dam area
        self.hartbeespoort_dam_center = [27.8486, -25.7478]
        print(f"Center: {self.hartbeespoort_dam_center}")
        self.buffer_distance = 3500  # in meters
        print(f"Buffer Distance: {self.buffer_distance}")
        self.hartbeespoort_dam = ee.Geometry.Polygon(self.get_rectangle(self.hartbeespoort_dam_center, self.buffer_distance))
        print("rectangle drawn...")


    def get_rectangle(self, center, distance):
        lat, lon = center
        delta_deg = distance / 111320  # Convert meters to degrees (approximation)
        return [
            [lat - delta_deg, lon - delta_deg],
            [lat - delta_deg, lon + delta_deg],
            [lat + delta_deg, lon + delta_deg],
            [lat + delta_deg, lon - delta_deg]
        ]

    # Function to get image collection for a specific date range
    def get_image_collection(self, start_date, end_date):
        print("Collection starting...")
        return (ee.ImageCollection('COPERNICUS/S2')
                .filterBounds(self.hartbeespoort_dam)
                .filterDate(start_date, end_date)
                .filter(ee.Filter.lt('CLOUDY_PIXEL_PERCENTAGE', 10)))

    # Function to process each image
    def process_image(self, image):
        # Select the RGB bands
        rgb = image.select(['B4', 'B3', 'B2'])

        # Apply the visual parameters
        visParams = {
            'bands': ['B4', 'B3', 'B2'],
            'min': 0,
            'max': 3000,
            'gamma': 1.2
        }

        visualized = rgb.visualize(**visParams)

        # Clip to the area of interest
        return visualized.clip(self.hartbeespoort_dam)

    # Function to download images for a specific time range
    def download_images_for_range(self, start_date, end_date, folder_name):
        print("Connecting to satellite...")
        collection = self.get_image_collection(start_date, end_date)
        print("Images collected")
        processed = collection.map(self.process_image)
        image_list = processed.toList(processed.size())
        date_list = collection.aggregate_array('system:time_start')

        # Create folder if it doesn't exist
        if not os.path.exists(folder_name):
            os.makedirs(folder_name)

        # Download images
        size = image_list.size().getInfo()
        dates = date_list.getInfo()

        for i in range(size):
            image = ee.Image(image_list.get(i))

            # Get the date from the image properties
            if i < len(dates) and dates[i] is not None:
                date = datetime.fromtimestamp(dates[i] / 1000).strftime('%Y-%m-%d')
            else:
                date = f"unknowndate{i}"

            filename = os.path.join(folder_name, f'hartbeespoortdam{date}.tif')

            # Download the image using geemap
            geemap.ee_export_image(
                image,
                filename=filename,
                scale=10,  # 10m resolution, same as Sentinel-2
                region=self.hartbeespoort_dam,
                file_per_band=False
            )
            print(f'Downloaded: {filename}')

        return True



