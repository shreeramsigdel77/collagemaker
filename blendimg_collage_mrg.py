import numpy as np
import cv2
from os import listdir
from os.path import splitext

from time import time


collage_img_path = "/home/pasonatech/labelme/collage_img-maker/collage/"
blend_img_path = "/home/pasonatech/blender_proc/BlenderProc-master/examples/crescent_test/output_randCrescent/coco_data/" # this one has transparency
dst_dir = "/home/pasonatech/blender_proc/BlenderProc-master/examples/crescent_test/collage_merged_img/"
def loadImage(path):
    n_imgList = []
    imgList = listdir(path)
    imgList.sort()
    for x in imgList:
        x_name, x_ext = x.split(".")
        if x_ext in ("png","jpg","JPEG"): #add new image extention as required
            n_imgList.append(x)
    return n_imgList
    
def img_match(c_path,c_List,b_path,b_List, o_path):
    loadedImg = []
    for c_imgName, b_imgName in zip(c_List,b_List):
        print(f"img {c_imgName}{b_imgName}")
        e_imgName, ext = splitext(b_imgName)
        print(ext)
        if ext == ".png":
    
            img1 = cv2.imread(c_path + c_imgName, -1)
            img2 = cv2.imread(b_path + b_imgName, -1) #with transparent background

            #image overlays
            result_img = img_overlays(img1, img2)
            filename = o_path+b_imgName
            cv2.imwrite(filename,result_img)
            # loadedImg.append(img)

def img_overlays(img1,img2):
    h, w, c = img2.shape
    img1 = cv2.resize(img1, (w, h), interpolation = cv2.INTER_CUBIC)
    result = np.zeros((h, w, 3), np.uint8)

    #slow
    # st = time()
    # for i in range(h):
    #     for j in range(w):
    #         color1 = img1[i, j]
    #         color2 = img2[i, j]
    #         alpha = color2[3] / 255.0
    #         new_color = [ (1 - alpha) * color1[0] + alpha * color2[0],
    #                       (1 - alpha) * color1[1] + alpha * color2[1],
    #                       (1 - alpha) * color1[2] + alpha * color2[2] ]
    #         result[i, j] = new_color
    # end = time() - st
    # print(end)

    #fast
    st = time()
    alpha = img2[:, :, 3] / 255.0
    result[:, :, 0] = (1. - alpha) * img1[:, :, 0] + alpha * img2[:, :, 0]
    result[:, :, 1] = (1. - alpha) * img1[:, :, 1] + alpha * img2[:, :, 1]
    result[:, :, 2] = (1. - alpha) * img1[:, :, 2] + alpha * img2[:, :, 2]
    end = time() - st
    print(end)

    
    cv2.imshow("result", result)
    cv2.waitKey(1000)
    cv2.destroyAllWindows()
    return result


# img_overlays(img1,img2)
collage_imgList = loadImage(collage_img_path)
blend_imgList = loadImage(blend_img_path)
img_match(collage_img_path, collage_imgList, blend_img_path, blend_imgList, dst_dir)
print("Merged")
# print(collage_imgList)
# print(blend_imgList)