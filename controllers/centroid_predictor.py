from sqlalchemy import create_engine
import sqlite3
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeRegressor
from sklearn.metrics import mean_squared_error
from models.db import VegetationDatabase


class PredictionModel:
    def __init__(self):
        self.db = VegetationDatabase()
        self.engine = create_engine('sqlite:///vegetation.db')
        self.model = DecisionTreeRegressor()

    def load_data(self):
        # Connect to the database and fetch the vegetation features
        query = '''
            SELECT date, vegetation_id, centroid_x, centroid_y, area, bbox_x, bbox_y, bbox_width, bbox_height,
                   aspect_ratio, relative_position_x, relative_position_y
            FROM vegetation_features
        '''
        df = pd.read_sql_query(query, self.engine)

        # Prepare data: shift centroid columns to create target variables
        print("Preparing data...")
        df = df.sort_values(by=['date', 'vegetation_id'])
        df['next_centroid_x'] = df['centroid_x'].shift(-1)
        df['next_centroid_y'] = df['centroid_y'].shift(-1)
        df = df.dropna(subset=['next_centroid_x', 'next_centroid_y'])

        # Define features (X) and targets (y)
        features = ['centroid_x', 'centroid_y', 'area', 'aspect_ratio', 'relative_position_x', 'relative_position_y']
        X = df[features]
        y = df[['next_centroid_x', 'next_centroid_y']]
        print("Data successfully prepared!!")
        return X, y, df

    def train_model(self):
        # Load data and split into training and testing sets
        X, y, _ = self.load_data()
        print("Splitting data for test and training...")
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

        # Train the model
        self.model.fit(X_train, y_train)

        # Evaluate the model
        predictions = self.model.predict(X_test)
        mse = mean_squared_error(y_test, predictions)
        print("Mean Squared Error:", mse)

    def predict_and_store(self):
        # Load data and make predictions for the next centroid locations
        X, _, data_df = self.load_data()

        # Make predictions
        predictions = self.model.predict(X)

        # Add predictions to the dataframe
        data_df['predicted_centroid_x'] = predictions[:, 0]
        data_df['predicted_centroid_y'] = predictions[:, 1]

        # Store predictions in the database
        self.db.store_prediction_data(data_df)
