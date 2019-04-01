import numpy as np
import argparse
import cv2


def sort_contours(cnts, method="left-to-right"):
    # initialize the reverse flag and sort index
    reverse = False
    i = 1
 
    # handle if we need to sort in reverse
    if method == "right-to-left" or method == "bottom-to-top":
	    reverse = True
 
    # handle if we are sorting against the y-coordinate rather than
    # the x-coordinate of the bounding box
    if method == "top-to-bottom" or method == "bottom-to-top":
	    i = 1
 
    # construct the list of bounding boxes and sort them from top to
    # bottom
    boundingBoxes = [cv2.boundingRect(c) for c in cnts]
    (cnts, boundingBoxes) = zip(*sorted(zip(cnts, boundingBoxes),
    	key=lambda b:b[1][i], reverse=reverse))
 
    # return the list of sorted contours and bounding boxes
    return cnts



def mser_th_value(rows,cols):
    
    min_th = int(0)
    max_th = int(0)

    if (rows <= 500):
        min_th = rows/10 + 20
    if (rows > 500):
        min_th = rows/6 +40
    if (cols < 300):
        max_th = cols
    elif ( cols < 1500):
        max_th = cols*2+500
    else:
        max_th = cols*5+900
    return min_th, max_th

image = cv2.imread('D:/works/New folder/03-OUTPUT1.png',0)

rows, cols = image.shape

min_th, max_th = mser_th_value(rows, cols)
    

mser = cv2.MSER_create(2, min_th, max_th, 0.05, 2, 200, 1.01, 0.003, 5)

vis = cv2.imread('D:/works/New folder/03-OUTPUT1.png')

regions = mser.detectRegions(image, None)

regions = sort_contours(regions, method="left-to-right")

#Checking the area cover by MSER
hulls = [cv2.convexHull(p.reshape(-1, 1, 2)) for p in regions]

cv2.polylines(vis, hulls, 1, (0, 0, 255))


#Segmentation section 
min_row =0
min_col =0
max_row =0
max_col =0
a=0

for i in regions:
    min_row = (min(i[:,1]))-1
    max_row = (max(i[:,1]))+1
    min_col = (min(i[:,0]))-1
    max_col = (max(i[:,0]))+1
    print a

    n_row = max_row - min_row
    n_col = max_col - min_col
    j=0
    k=0
    next_image = np.zeros((n_row, n_col), dtype=np.uint8)
    
    for j in range(0,n_row):
        for k in range(0,n_col):
            next_image[j][k] = image[min_row+j][min_col+k]
    
    cv2.imwrite('D:/test/image%d.png'%(a),next_image)
    a=a+1

cv2.imwrite("test1.png", vis)






