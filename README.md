# Object detection by Opencv
####Input image;
![](https://github.com/PudPawat/object-detection-by-openCV/blob/main/images/start.jpg?raw=true width="100")
####Mask image;
![](https://github.com/PudPawat/object-detection-by-openCV/blob/main/images/mask.jpg?raw=true width="100")
####Final image;
![](https://github.com/PudPawat/object-detection-by-openCV/blob/main/images/final.jpg?raw=true width="100")


### Algorithm

- Using HSV inrange to filter background out;
- Find contours and min rectangel box of the contour(Example case biggest one); 
- Then put all pixel in the contour into black image. So we get mask image;
- Rotate and crop to be final image;
