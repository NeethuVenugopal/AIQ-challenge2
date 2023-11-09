import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

from PIL import Image

import mysql.connector
import os
from dotenv import load_dotenv
from io import BytesIO

# Load environment variables from the .env file
load_dotenv()


#Function to read image from csv
def read_image(csv_file):
    # Read the Excel data
    df = pd.read_csv(csv_file)

    image_data = df.iloc[:, 1:201].values.astype('uint8')

    print(image_data.shape)

    # plt.imshow(image_data, cmap='gray') 
    # plt.axis('off')  # Hide axis labels
    # plt.title(f"Depth Image")
    # plt.show()
    return image_data

#Function to resize image to width 150 keeping aspect ratio
def resize_image(image_data,new_width):
    img = Image.fromarray(image_data)
    print(f'image size before resizing:{img.size}')
    width_percent = (new_width / float(img.size[0]))
    new_height = int(float(img.size[1]) * width_percent)
    img = img.resize((new_width, new_height), Image.LANCZOS)
    print(f'image size after resizing:{img.size}')
    return img

#Function to save image to database
def store_image(img):
    # Establish the MySQL database connection
    try:
        connection = mysql.connector.connect(
            host = os.getenv("HOST"),
            user = os.getenv("USER"),
            password = os.getenv("MYSQLPASS"),
            database="imagedb"
        )

        if connection.is_connected():
            print("Connected to MySQL database")
            # Create a cursor to interact with the database
            cursor = connection.cursor()

            # Define the table structure 
            create_table_query = """
            CREATE TABLE IF NOT EXISTS images (
                id INT AUTO_INCREMENT PRIMARY KEY,
                image_data MEDIUMBLOB
            )
            """

            cursor.execute(create_table_query)
            connection.commit()
            
            # Convert the image to bytes
            image_bytes = BytesIO()
            img.save(image_bytes, format='png')

            # Insert the image data into the database table
            insert_query = "INSERT INTO images (image_data) VALUES (%s)"
            cursor.execute(insert_query, (image_bytes.getvalue(),))
            connection.commit()


    except mysql.connector.Error as e:
        print(f"Error: {e}")
    finally:
        if connection.is_connected():
            # Close the cursor and the database connection
            cursor.close()
            connection.close()
            print("Connection to MySQL database closed")



if __name__ == "__main__":
    csv_file = "AIQ - Machine Learning Engineer Assignment - Data.csv"
    image_data = read_image(csv_file)
    resized_image = resize_image(image_data,150)
    store_image(resized_image)
