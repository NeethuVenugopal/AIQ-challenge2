import requests
import base64
from PIL import Image
import io
import matplotlib.pyplot as plt

url = "http://127.0.0.1:8000/"
endpoint = "frames/"
params = {"depth_min" : 10,
          "depth_max" : 500
}

response = requests.get(url = url + endpoint, params=params)
imageb64list = response.json()
# Create a subplot grid for displaying images
num_frames = len(imageb64list)
num_cols = 3  # Adjust the number of columns as needed
num_rows = (num_frames + num_cols - 1) // num_cols

# Set up the subplot grid
fig, axes = plt.subplots(num_rows, num_cols, figsize=(12, 8))


for i, imgb64 in enumerate(imageb64list):
    
    ax = axes[i]

    image_data = base64.b64decode(imgb64)
    pil_image = Image.open(io.BytesIO(image_data))
    
    ax.imshow(pil_image)
    ax.set_title(f"Frame {i+1}")

    # Remove axis labels and ticks
    ax.axis('off')

for i in range(num_frames, num_rows * num_cols):
    fig.delaxes(axes[i])
plt.tight_layout()

# Show the image frames
plt.show()
