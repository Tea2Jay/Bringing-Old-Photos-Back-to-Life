import argparse
import shutil
import sys
from glob import glob
import argparse
import numpy as np
from PIL import Image
from tqdm import tqdm

# np.set_printoptions(threshold=sys.maxsize)
# print(sys.argv[1])
# prev_mask_path = masks_paths.pop(0)
# prev_mask = np.array(Image.open(prev_mask_path).convert('L'), np.int64)
parser = argparse.ArgumentParser()
parser.add_argument('--frames', type=int,required=True)


def mask_intersection(masks_paths, num_of_intersections, dir_to_save):

    for mask_path in tqdm(masks_paths[:num_of_intersections]):
        shutil.copyfile(mask_path, dir_to_save + mask_path.split("\\")[-1])

    for mask_path in tqdm(masks_paths[-num_of_intersections:]):
        shutil.copyfile(mask_path, dir_to_save + mask_path.split("\\")[-1])

    for mask_path in tqdm(masks_paths[num_of_intersections:-num_of_intersections]):

        intersection = intersection_of_next_and_prev_n_frames(
            num_of_intersections, masks_paths, masks_paths.index(mask_path)
        )
        intersection = np.where(intersection == True, 255, intersection)
        # print(f"{intersection=}")
        t = np.unique(intersection)
        print(t)
        
        frame = Image.fromarray(np.uint8(intersection),mode='L')
        
        path_to_save_mask = dir_to_save + mask_path.split("\\")[-1]
        frame.save(path_to_save_mask)


def intersection_of_next_and_prev_n_frames(number_of_intersections, mask_list, index):

    intersected_mask = np.array(Image.open(mask_list[index]).convert("L"), np.bool_)
    # print(f"{intersected_mask=}")
    for intersection in range(number_of_intersections):
        next_mask = np.array(
            Image.open(mask_list[index + intersection + 1]).convert("L"), np.bool_
        )
        # print(f"{next_mask=}")
        
        prev_mask = np.array(
            Image.open(mask_list[index - intersection - 1]).convert("L"), np.bool_
        )
        # print(f"{prev_mask=}")
        k = intersected_mask & prev_mask & next_mask
        print(f"{np.unique(k)=}")
        
        intersected_mask = intersected_mask & prev_mask & next_mask
        print(f"{np.unique(intersected_mask)=}")

    return intersected_mask


def flicker_removal(original, mask, removed, dir_to_save):

    original.sort()
    mask.sort()
    removed.sort()

    all = zip(original, mask, removed)

    for o, m, a in tqdm(all):
        frame_n = o.split("\\")[-1].split(".")[0]
        o = np.array(Image.open(o))
        m = np.array(Image.open(m), dtype=np.bool_)
        a = np.array(Image.open(a))
        # om = o * ~m
        # ma = m * a
        flicker_removed = (o * (~m)) + (m * a)
        flicker_removed = Image.fromarray(flicker_removed)
        # om = Image.fromarray(om)
        # ma = Image.fromarray(ma)

        flicker_removed.save(dir_to_save + frame_n + ".png")
        # om.save("./tmp/om_" + frame_n + ".png")
        # ma.save("./tmp/ma_" + frame_n + ".png")


if __name__ == "__main__":

    # original = glob(".\\data\\output\\*")
    # mask = glob(".\\data\\mask\\*")
    # arti_removed = glob(".\\data\\final_output\\*")

    # flicker_removal(original, mask, arti_removed, ".\\data\\non_flicker\\")
    arg = parser.parse_args()
    
    masks_paths = glob(".\\data\\mask\\*")
    masks_paths.sort()
    masks_paths = masks_paths[50:60]
    num_of_intersections = arg.frames
    dir_to_save = ".\\data\\mask_intersection_1_frame\\"
    # print(f"{masks_paths=}")
    mask_intersection(masks_paths, num_of_intersections, dir_to_save)
