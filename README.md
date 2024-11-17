# Aquatic Weeds Predictive System

This application is designed to predict and analyze aquatic weed growth using satellite imagery and machine learning techniques.

## Prerequisites

Before running the application, ensure you have the following:

1. Python 3.x installed on your system
2. Required Python packages (list them here or reference a requirements.txt file)
3. A Google Earth Engine account and project

## Setup

1. Clone the repository:
   ```
   git clone https://github.com/ShiiFt38/Aquatic-Weeds-Predictive-System.git
   cd Aquatic-Weeds-Predictive-System
   ```

2. Install the required packages:
   ```
   pip install -r requirements.txt
   ```

3. Create a `.env` file in the root directory of the project with your Google Earth Engine project ID:
   ```
   EarthEngine_Project=your_project_id_here
   ```

   This file is required for the `satellite_imagery.py` script to access Google Earth Engine services.

## Running the Application

To start the application, run:

```
python app.py
```

## Project Structure

- `app.py`: Main application entry point
- `controllers/`: Contains backend logic
  - `image_processor.py`: Handles image processing tasks
  - `downloader.py`: Manages data downloading
  - `satellite_imagery.py`: Interacts with Google Earth Engine (requires .env file)
  - `image_processor.py`: Handles image processing tasks
  - `downloader.py`: Manages data downloading, including weather and satellite data
  - `satellite_imagery.py`: Interacts with Google Earth Engine (requires .env file)
  - `centroid_predictor.py`: Implements a decision tree machine learning model to predict vegetation centroid locations based on input features and historical data
  - `weather_handler.py`: Retrieves and processes weather data from APIs, managing the integration of historical and real-time weather information
- `views/`: Contains frontend UI components
  - `dashboard_win.py`: Dashboard window
  - `data_win.py`: Data visualization window
  - `login_win.py`: Login window
  - `reports_win.py`: Reports generation window
  - `ui.py`: Main UI components
  - `settings_dialog.py`: Settings management
  - `loading_screen.py`: Displays a visually engaging loading screen during backend operations like data fetching and processing
- `models/` : Database utilities
  - `db.py`: Database creation and CRUD functions
  - `db_export_utility`: Dedicated file exporting module
- `utilities/` 
  - `file_exporter.py`: Exports processed data and results in formats like CSV and PDF
  - `gemini_assistant.py`: AI-driven assistant to provide insights about uploaded images, with a focus on vegetation detection
  - `custom_pdf.py`: Generates professional PDF reports summarizing vegetation predictions, weather insights, and centroid forecasts

## Contributing

To contribute to the project:

1. Create a new branch for your feature or bug fix
2. Make your changes
3. Test thoroughly
4. Create a pull request with a clear description of your changes


