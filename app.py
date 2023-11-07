from fastapi import FastAPI, HTTPException, Query
from PIL import Image
from io import BytesIO
import mysql.connector
from dotenv import load_dotenv
import os
import matplotlib as mpl
import numpy as np

# Load environment variables from the .env file
load_dotenv()

# Access environment variables
db_host = "Localhost"
db_user = "root"
db_password = os.getenv("MYSQLPASS")
db_name = "imagedb"

# Create a FastAPI app
app = FastAPI()

# Establish a connection to the MySQL database
connection = mysql.connector.connect(
    host=db_host,
    user=db_user,
    password=db_password,
    database=db_name
)

# Create a cursor to interact with the database
cursor = connection.cursor()

def crop_image(image, row_min, row_max):
    width, height = image.size
    if row_min < 0 or row_max > height or row_min >= row_max:
        raise ValueError("Invalid row range provided.")

    # Crop the image to include only the specified rows
    cropped_image = image.crop((0, row_min, width, row_max))
    return cropped_image

def apply_colormap(image):
    cdict = {'red': ((0.0, 0.0, 0.0),
                 (0.1, 0.5, 0.5),
                 (0.2, 0.0, 0.0),
                 (0.4, 0.2, 0.2),
                 (0.6, 0.0, 0.0),
                 (0.8, 1.0, 1.0),
                 (1.0, 1.0, 1.0)),
        'green':((0.0, 0.0, 0.0),
                 (0.1, 0.0, 0.0),
                 (0.2, 0.0, 0.0),
                 (0.4, 1.0, 1.0),
                 (0.6, 1.0, 1.0),
                 (0.8, 1.0, 1.0),
                 (1.0, 0.0, 0.0)),
        'blue': ((0.0, 0.0, 0.0),
                 (0.1, 0.5, 0.5),
                 (0.2, 1.0, 1.0),
                 (0.4, 1.0, 1.0),
                 (0.6, 0.0, 0.0),
                 (0.8, 0.0, 0.0),
                 (1.0, 0.0, 0.0))}

    cust_cmap = mpl.colors.LinearSegmentedColormap('my_colormap',cdict,256)
    im = np.array(image)
    im = cust_cmap(im)
    img = Image.fromarray((im[:, :, :3] * 255).astype(np.uint8))
    img.save('test.png')
    return img

@app.get("/frames/")
def retrieve_images(depth_min: int, depth_max: int):
    try:
        # Retrieve image data from the database within the specified row range
        retrieve_query = "SELECT image_data FROM images"
        cursor.execute(retrieve_query)
        rows = cursor.fetchall()

        if not rows:
            raise HTTPException(status_code=404, detail="No images found.")

        images = []

        for row in rows:
            # Load image data from the database and apply a custom colormap
            image_data = row[0]
            image = Image.open(BytesIO(image_data))
            # Apply your custom colormap here (modify as needed)
            image = crop_image(image, depth_min, depth_max)
            color_image = apply_colormap(image)
            print(image.size)
            images.append(list(image.getdata()))

        return images

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="localhost", port=8000)
