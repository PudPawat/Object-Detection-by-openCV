import cv2 as cv
import os
import numpy as np 
import imutils

def img_process(img):
    ### Binary by HSV inrange ###
    low_H, low_S, low_V, high_H, high_S, high_V = [30, 0, 0, 137, 255, 255]
    frame_HSV = cv.cvtColor(img, cv.COLOR_BGR2HSV)
    frame_threshold = cv.inRange(frame_HSV, (low_H, low_S, low_V), (high_H, high_S, high_V))

    kernel_size = 8
    kernel = cv.getStructuringElement(cv.MORPH_ELLIPSE, (kernel_size, kernel_size))
    frame_erode = cv.erode(frame_threshold, kernel)
    kernel_size = 12
    kernel = cv.getStructuringElement(cv.MORPH_ELLIPSE, (kernel_size, kernel_size))
    frame_dilate = cv.dilate(frame_erode, kernel)

    return frame_dilate

def find_min_box(bi_img,img):
    
    ### find contours ##
    contours, __ = cv.findContours(bi_img, cv.RETR_TREE, cv.CHAIN_APPROX_NONE)
    print(contours)

    areas = []
    for contour in contours:
        # print(co)
        area = cv.contourArea(contour)
        areas.append(area)

    max_area = max(areas)
    index = []
    for i , area in enumerate(areas):
        if area == max_area:
            index = i
            break

    max_contour = contours[index]
    # print(max_contour[index].shape)
    min_rec = cv.minAreaRect(max_contour)
    print(len(min_rec))
    box = cv.boxPoints(min_rec)
    box = np.int0(box)
    print(len(box))
    # print(box.shape)
    print(min_rec)
    img = cv.drawContours(img,[box], 0, (0, 0, 255), 5)

    # cv.namedWindow("output", cv.WINDOW_NORMAL)  # Create window with freedom of dimensions
    # cv.resizeWindow("output", int(img.shape[1]/2), int(img.shape[0]/2))
    # cv.imshow("output",img)
    # cv.waitKey(0)
    return min_rec

def mask_img(img, minrec_box):
    if len(minrec_box) == 3 :
        box = cv.boxPoints(minrec_box)
        box = np.int0(box)
    else:
        box = minrec_box

    mask_contour = np.zeros(img.shape[0:2], np.uint8)
    cv.drawContours(mask_contour, [box], -1, (255, 255, 255), 3)
    cv.fillPoly(mask_contour, pts=[box], color=(255, 255, 255))
    masked_both = cv.bitwise_and(img, img, mask=mask_contour)
    # cv.imshow("aqaqa", masked_both)
    return mask_contour, masked_both


def crop_maskcontour(mask_contour,mask_bolt, minrec_box):
    rot_maskcon = imutils.rotate_bound(mask_contour, -minrec_box[2])
    rot_maskbolt = imutils.rotate_bound(mask_bolt, -minrec_box[2])
    imshow_fit("aaaaa",rot_maskbolt)
    cv.findContours(rot_maskcon, cv.RETR_TREE, cv.CHAIN_APPROX_NONE)
    rot_minrec_box = find_min_box(rot_maskcon,rot_maskbolt)
    box = cv.boxPoints(rot_minrec_box)
    box = np.int0(box)
    topleft = box.min(axis=0)
    botright = box.max(axis=0)
    crop_rot = rot_maskbolt[topleft[1]:botright[1],topleft[0]:botright[0]]

    return crop_rot

def imshow_fit(windowname,img):
    print(max(img.shape))
    print(img.shape)
    if max(img.shape) > 1300 and max(img.shape) < 3500:
        factor = 2.5
    elif max(img.shape) > 3500 and max(img.shape) < 5000:
        factor = 3.5
    elif max(img.shape) > 5000 :
        factor = 5
    else:
        factor = 1
    cv.namedWindow(windowname,cv.WINDOW_GUI_NORMAL)  # Create window with freedom of dimensions
    cv.resizeWindow(windowname, int(img.shape[1]/factor), int(img.shape[0]/factor))
    cv.imshow(windowname, img)
    cv.waitKey(0)



def main():
    img = cv.imread("data/4.jpg")
    imshow_fit("original",img)
    imgproc = img_process(img)
    ori_min_rect = find_min_box(imgproc,img)
    binary_mask, ori_mask = mask_img(img,ori_min_rect)
    crop_obj = crop_maskcontour(binary_mask,ori_mask,ori_min_rect)
    imshow_fit("crop_object",crop_obj)

    # cv.waitKey(0)



# def rotateImage(image, angle):
#    (h, w) = image.shape[:2]
#    center = (w / 2, h / 2)
#    M = cv.getRotationMatrix2D(center,angle,1.0)
#    rotated_image = cv.warpAffine(image, M, (w,h))
#    return rotated_image

if __name__ =="__main__":
    # img = cv.imread("data/Image__2020-11-22__22-51-14.jpg")
    # img = cv.imread("data/4.jpg")
    # minrect, masked = find_min_box(img)
    main()




    # img_rot = rotateImage(masked,minrect[2])
    # rotated = imutils.rotate_bound(masked, -minrect[2])
    # cv.imshow("asd",img_rot)
    # cv.imshow("asda", rotated)
    # cv.waitKey(0)