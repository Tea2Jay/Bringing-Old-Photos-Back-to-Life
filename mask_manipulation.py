import argparse
import os
import shutil
import sys
from glob import glob
import argparse
import numpy as np
from PIL import Image
from tqdm import tqdm
from tqdm.contrib.concurrent import process_map, thread_map

# np.set_printoptions(threshold=sys.maxsize)
# print(sys.argv[1])
# prev_mask_path = masks_paths.pop(0)
# prev_mask = np.array(Image.open(prev_mask_path).convert('L'), np.int64)
parser = argparse.ArgumentParser()
parser.add_argument("--frames", type=int)
parser.add_argument("--interval", nargs="+", type=int)


def mask_intersection(masks_paths, num_of_intersections, dir_to_save):

    for mask_path in tqdm(masks_paths[:num_of_intersections]):
        shutil.copyfile(mask_path, dir_to_save + mask_path.split("/")[-1])

    for mask_path in tqdm(masks_paths[-num_of_intersections:]):
        shutil.copyfile(mask_path, dir_to_save + mask_path.split("/")[-1])

    for mask_path in tqdm(masks_paths[num_of_intersections:-num_of_intersections]):

        intersection = intersection_of_next_and_prev_n_frames(
            num_of_intersections, masks_paths, masks_paths.index(mask_path)
        )
        intersection = np.where(intersection == True, 255, intersection)
        # print(f"{intersection=}")
        # t = np.unique(intersection)

        frame = Image.fromarray(np.uint8(intersection), mode="L")

        path_to_save_mask = dir_to_save + mask_path.split("/")[-1]
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
        # print(f"{np.unique(k)=}")

        intersected_mask = intersected_mask & prev_mask & next_mask
        # print(f"{np.unique(intersected_mask)=}")

    return intersected_mask


def flicker_removal(original, mask, arti_removed):

    all = zip(original, mask, arti_removed)

    for o, m, a in tqdm(all, total=len(original)):
        frame_n = o.split("/")[-1].split(".")[0]

        o = np.array(Image.open(o))
        m = np.array(Image.open(m), dtype=np.bool_)
        a = np.array(Image.open(a))

        flicker_removed = (o * (~m)) + (m * a)
        flicker_removed = Image.fromarray(flicker_removed)

        flicker_removed.save(dir_to_save + frame_n + ".png")


def flicker_removal_multiprocessing(original, mask, arti_removed):

    frame_n = original.split("/")[-1].split(".")[0]

    original = np.array(Image.open(original))
    mask = np.array(Image.open(mask), dtype=np.bool_)
    arti_removed = np.array(Image.open(arti_removed))

    flicker_removed = (original * (~mask)) + (mask * arti_removed)
    flicker_removed = Image.fromarray(flicker_removed)

    flicker_removed.save(dir_to_save + frame_n + ".png")


if __name__ == "__main__":

    global dir_to_save

    arg = parser.parse_args()

    original = glob("./data/colorized_input/*")
    masks_paths = glob("./data/mask/*")
    arti_removed = glob("./data/final_output/*")

    original.sort()
    masks_paths.sort()
    arti_removed.sort()

    # num_of_intersections = arg.frames
    # s_slice = arg.interval[0]
    # e_slice = arg.interval[1]
    # masks_paths = masks_paths[s_slice:e_slice]

    dir_to_save = "./data/flicker_removed_colorized/"
    os.makedirs(dir_to_save, exist_ok=True)
    # print(f"{masks_paths=}")
    # mask_intersection(masks_paths, num_of_intersections, dir_to_save)

    # flicker_removal(original, masks_paths, arti_removed, "./data/flicker_removed/")
    process_map(
        flicker_removal_multiprocessing,
        original,
        masks_paths,
        arti_removed,
        max_workers=60,
        chunksize=100,
    )
