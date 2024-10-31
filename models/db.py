import sqlite3 as sq


class VegetationDatabase:
    def __init__(self, db_path='vegetation.db'):
        self.db_path = db_path
        self.conn = None
        self.setup_database()

    def setup_database(self):
        print("Connecting to Database")
        try:
            self.conn = sq.connect(self.db_path)
            print("Connection success")
        except sq.Error as e:
            print(f"Database connection error: {e}")
            return

        cursor = self.conn.cursor()

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS image_scans (
                date TEXT PRIMARY KEY NOT NULL,
                image_path TEXT,
                total_vegetation_count INTEGER,
                time_scanned TEXT
            )
        ''')

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS vegetation_features (
                feature_id INTEGER PRIMARY KEY AUTOINCREMENT,
                date TEXT,
                vegetation_id INTEGER,
                area REAL,
                bbox_x INTEGER,
                bbox_y INTEGER,
                bbox_width INTEGER,
                bbox_height INTEGER,
                centroid_x INTEGER,
                centroid_y INTEGER,
                aspect_ratio REAL,
                relative_position_x REAL,
                relative_position_y REAL,
                FOREIGN KEY (date) REFERENCES image_scans(date)
            )
        ''')

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS weather_data (
                weather_id INTEGER PRIMARY KEY AUTOINCREMENT,
                date TEXT,
                max_temp TEXT,
                min_temp TEXT,
                precipitation TEXT,
                rainfall TEXT,
                max_wind TEXT,
                FOREIGN KEY (date) REFERENCES image_scans(date)
            )
        ''')

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS vegetation_predictions (
                prediction_id INTEGER PRIMARY KEY AUTOINCREMENT,
                date TEXT,
                vegetation_id INTEGER,
                predicted_centroid_x INTEGER,
                predicted_centroid_y INTEGER,
                model_used TEXT,
                FOREIGN KEY (date) REFERENCES image_scans(date)
            )
        ''')

        self.conn.commit()

    def store_scan_data(self,image_path, vegetation_data):
        """Store a complete scan including all vegetation features."""
        cursor = self.conn.cursor()

        vegetation_count = len(vegetation_data)
        if vegetation_count == 0:
            print("No vegetation data to store.")
            return


        # Process and store each vegetation feature
        for veg in vegetation_data:
            x, y, w, h = veg['bounding_box']
            cx, cy = veg['centroid']

            # Calculate additional features
            aspect_ratio = w / h if h != 0 else 0
            # Normalize positions relative to image bounds (assuming 600x600 image)
            rel_x = cx / 600  # Adjust based on your actual image dimensions
            rel_y = cy / 600

            cursor.execute('''
                INSERT INTO vegetation_features (
                    date, area, vegetation_id, 
                    bbox_x, bbox_y, bbox_width, bbox_height,
                    centroid_x, centroid_y, aspect_ratio,
                    relative_position_x, relative_position_y
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                image_path[-14:-4], veg['area'], veg['id'],
                x, y, w, h,
                cx, cy, aspect_ratio,
                rel_x, rel_y
            ))

        self.conn.commit()

    def store_image_data(self, image_path, vegetation_data, time):
        cursor = self.conn.cursor()

        # 'Ignore into' handles primary key violations
        cursor.execute('''
            INSERT OR IGNORE INTO image_scans (date, image_path, total_vegetation_count, time_scanned)
            VALUES (?, ?, ?, ?)
        ''', (image_path[-14:-4], image_path, len(vegetation_data), time))
        print("Data Stored Successfully!")
        self.conn.commit()

    def store_weather_data(self, weather_data):
        cursor = self.conn.cursor()

        cursor.execute('''
            INSERT INTO weather_data (date, max_temp, min_temp, precipitation, rainfall, max_wind)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (weather_data['date'], weather_data['max_temp'], weather_data['min_temp'], weather_data['precipitation'],
              weather_data['rain'],weather_data['max_windspeed']))

        self.conn.commit()

    def store_prediction_data(self, data_df):
        cursor = self.conn.cursor()
        for _, row in data_df.iterrows():
            cursor.execute('''
                        INSERT INTO vegetation_predictions (date, vegetation_id, predicted_centroid_x, predicted_centroid_y, model_used)
                        VALUES (?, ?, ?, ?, ?)
                    ''', (row['date'], row['vegetation_id'], row['predicted_centroid_x'], row['predicted_centroid_y'],
                          'DecisionTree'))
        self.conn.commit()

    def get_training_data(self):
        """Retrieve formatted data for training the model."""
        cursor = self.conn.cursor()

        cursor.execute('''
            SELECT 
                area, bbox_width, bbox_height, aspect_ratio,
                relative_position_x, relative_position_y,
                centroid_x, centroid_y
            FROM vegetation_features
        ''')

        # Format data for machine learning
        features = []
        targets = []

        for row in cursor.fetchall():
            # Features: area, width, height, aspect_ratio, rel_pos_x, rel_pos_y
            features.append(list(row[:-2]))
            # Targets: centroid coordinates
            targets.append(list(row[-2:]))

        return features, targets

    def delete_all_data(self):
        """Delete all data from both tables in the database."""
        cursor = self.conn.cursor()

        # Delete all records from both tables
        cursor.execute("DELETE FROM vegetation_features")
        cursor.execute("DELETE FROM image_scans")
        cursor.execute("DELETE FROM weather_data")
        cursor.execute("DELETE FROM vegetation_predictions")
        cursor.execute("DELETE FROM sqlite_sequence WHERE name='vegetation_features' "
                       "OR name='image_scans' "
                       "OR name='weather_data' "
                       "OR name='vegetation_predictions'")

        self.conn.commit()
        return cursor.rowcount

    def get_history_prediction(self):
        cursor = self.conn.cursor()

        cursor.execute('''
                       SELECT
                            v.vegetation_id, 
                           i.date,
                           i.image_path,
                           i.total_vegetation_count,
                           SUM(v.area) as total_area,
                           AVG(v.area) as avg_area,
                           w.max_temp,
                           w.min_temp,
                           w.precipitation,
                           w.rainfall, 
                           w.max_wind,
                           i.time_scanned
                       FROM image_scans i
                       LEFT JOIN vegetation_features v ON i.date = v.date
                       LEFT JOIN weather_data w ON i.date = w.date
                       GROUP BY i.date
                       ORDER BY i.time_scanned
                   ''')
        data = cursor.fetchall()

        return data

    def close(self):
        if self.conn:
            self.conn.close()

    def get_connection(self):
        return self.conn