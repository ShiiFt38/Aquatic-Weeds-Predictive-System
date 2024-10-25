import sqlite3
import json
from datetime import datetime


class VegetationDatabase:
    def __init__(self, db_path='vegetation.db'):
        self.db_path = db_path
        self.conn = None
        self.setup_database()

    def setup_database(self):
        print("Connecting to Database")
        try:
            self.conn = sqlite3.connect(self.db_path)
            print("Connection success")
        except sqlite3.Error as e:
            print(f"Database connection error: {e}")
            return  # Exit if connection fails

        cursor = self.conn.cursor()

        # Create tables
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS image_scans (
                scan_id INTEGER PRIMARY KEY AUTOINCREMENT,
                date TEXT NOT NULL,
                image_path TEXT,
                total_vegetation_count INTEGER
            )''')

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
                relative_position_y REAL
            )
        ''')

        self.conn.commit()

    def store_scan_data(self,image_path, vegetation_data):
        """Store a complete scan including all vegetation features."""
        cursor = self.conn.cursor()

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

    def store_image_data(self, image_path, vegetation_data):
        cursor = self.conn.cursor()

        # Insert scan record
        cursor.execute('''
            INSERT INTO image_scans (date, image_path, total_vegetation_count)
            VALUES (?, ?, ?)
        ''', (image_path[-14:-4], image_path, len(vegetation_data)))

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
        cursor.execute("DELETE FROM sqlite_sequence WHERE name='vegetation_features' OR name='image_scans'")

        self.conn.commit()
        return cursor.rowcount

    def get_history_prediction(self):
        cursor = self.conn.cursor()

        cursor.execute('''
                       SELECT 
                           i.scan_id,
                           i.timestamp,
                           i.image_path,
                           i.total_vegetation_count,
                           SUM(v.area) as total_area,
                           AVG(v.area) as avg_area
                       FROM image_scans i
                       LEFT JOIN vegetation_features v ON i.scan_id = v.scan_id
                       GROUP BY i.scan_id
                       ORDER BY i.timestamp DESC
                       LIMIT 10
                   ''')
        data = cursor.fetchall()

        return data

    def close(self):
        """Close the database connection."""
        if self.conn:
            self.conn.close()