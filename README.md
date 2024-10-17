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
- `views/`: Contains frontend UI components
  - `dashboard_win.py`: Dashboard window
  - `data_win.py`: Data visualization window
  - `login_win.py`: Login window
  - `reports_win.py`: Reports generation window
  - `ui.py`: Main UI components
  - `settings_dialog.py`: Settings management

## Contributing

To contribute to the project:

1. Create a new branch for your feature or bug fix
2. Make your changes
3. Test thoroughly
4. Create a pull request with a clear description of your changes


