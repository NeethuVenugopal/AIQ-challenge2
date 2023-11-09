# AIQ-challenge2
image processing based application

prerequisites:
Need to start a MYSQL server and create a database named ‘imagedb’. The environment variables need to be changed accordingly which includes MYSQL user, password and host.
#readandsave.py

1. Read the image from csv
2. Resize the image so that column width changes from 200 to 150
![image](https://github.com/NeethuVenugopal/AIQ-challenge2/assets/23374413/790ffb9f-2c44-490e-bb9a-a78d10479215)
 
3. Save the image in MYSQL database
 ![image](https://github.com/NeethuVenugopal/AIQ-challenge2/assets/23374413/8dfaba97-7c3f-44a8-8b3e-76492b50325a)

#app.py (Fast API app)

1. API to Retrieve the saved images from database (If there were one frame/depth level, we could retrieve only those frames between depth_min and depth_max )
 ![image](https://github.com/NeethuVenugopal/AIQ-challenge2/assets/23374413/6ed25aaa-e046-4fd0-890d-31707a9d985a)

2. Crop the image based on depth_min and depth_max () (image is cropped such that we remove rows below depth_min and above depth_max)
3. Apply custom color map to the cropped image
4. Return the resultant image as base64 string
5. Containerized the solution. Running the container will first call readandsave.py file and then run the app.py
#test.py

This program is used to test the API and convert the returned base64 strings to images and display it.
![image](https://github.com/NeethuVenugopal/AIQ-challenge2/assets/23374413/f8d0f96c-15fc-4626-873d-d806a4ec8464)
 
