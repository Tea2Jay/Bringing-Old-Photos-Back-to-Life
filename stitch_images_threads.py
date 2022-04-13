import numpy as np
import os
from glob import glob
from skimage import io, color
from tqdm import tqdm
from tqdm.contrib.concurrent import thread_map


def open_img(path):
    img = io.imread(path)
    if img.shape[2] < 3:
        img = color.gray2rgb(img)
    return img


def stitch_images(list_of_paths):
    file_path = list_of_paths[1].split("/")[-1]
    imgs = list(map(open_img, list_of_paths))
    con_img = np.concatenate(imgs, axis=1)
    io.imsave(out_dir + "/" + file_path, con_img)


out_dir = "./input_and_scratch_removed_v1_and_v2"
os.makedirs(out_dir, exist_ok=True)

imgA_list = glob("colorized_input/*")
imgA_list.sort()

imgB_list = glob("final_output/*")
imgB_list.sort()

imgC_list = glob("flicker_removed_colorized/*")
imgC_list.sort()

paths_list = zip(imgA_list, imgB_list, imgC_list)

thread_map(stitch_images, paths_list, max_workers=60, total=len(imgA_list))
# for i in tqdm(range(len(imgA_list))):
#     file_path = imgB_list[i].split("/")[-1]

#     fileA = imgA_list[i]
#     imgA = io.imread(fileA)
#     if imgA.shape[2] < 3:
#         imgA = color.gray2rgb(imgA)

#     fileB = imgB_list[i]
#     imgB = io.imread(fileB)
#     if imgB.shape[2] < 3:
#         imgB = color.gray2rgb(imgB)

#     out_img = np.concatenate(imgA_list,imgB_list)
#     io.imsave(out_dir + "/" + file_path, out_img)
