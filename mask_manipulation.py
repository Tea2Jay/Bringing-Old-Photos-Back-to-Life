import sys
from glob import glob

import numpy as np
from PIL import Image
from tqdm import tqdm

# print(sys.argv[1])
# prev_mask_path = masks_paths.pop(0)
# prev_mask = np.array(Image.open(prev_mask_path).convert('L'), np.int64)


def sum_of_next_and_prev_n(number_of_intersections, mask_list, index):

    intersected_mask = np.array(Image.open(mask_list[index]).convert("L"), np.int64)

    for intersection in range(number_of_intersections):
        next_mask = np.array(
            Image.open(mask_list[index + intersection + 1]).convert("L"), np.int64
        )
        prev_mask = np.array(
            Image.open(mask_list[index - intersection - 1]).convert("L"), np.int64
        )
        intersected_mask = np.add(np.add(prev_mask, intersected_mask), next_mask)

    return intersected_mask




if __name__ == "__main__":

    masks_paths = glob("./colorized_mask/mask/*")
    masks_paths.sort()

    num_of_intersections = int(sys.argv[1])
    for mask_path in tqdm(masks_paths[num_of_intersections:-1]):
        # print(mask_path)
        # next_mask = np.array(Image.open(masks_paths[num_of_mask_to_intersect+1]).convert('L'), np.int64)
        # mask = np.array(Image.open(mask_path).convert('L'), np.int64)
        # mask_combined = np.add(np.add(mask, prev_mask), next_mask)
        sum_of_n_masks = sum_of_next_and_prev_n(
            num_of_intersections, masks_paths, masks_paths.index(mask_path)
        )

        mask_cleaned = np.where((sum_of_n_masks == (255 * num_of_intersections)), 255)
        # print(np.unique(mask_combined))
        # mask_cleaned = np.where(mask_combined >= 765, 0, mask)
        # mask_cleaned = np.where(mask_cleaned == 765, 0, mask_cleaned)
        # prev_mask = mask

        mask_cleaned = mask_cleaned.astype(np.uint8)
        frame = Image.fromarray(mask_cleaned)
        path_to_save_mask = (
            "./colorized_mask/mask_intersection/" + mask_path.split("/")[-1]
        )
        # frame.save(path_to_save_mask)
