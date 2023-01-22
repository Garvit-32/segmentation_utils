import matplotlib.pyplot as plt
import numpy as np



import cv2

proto = ['WATER', 'ASPHALT', 'GRASS', 'HUMAN', 'ANIMAL', 'HIGH_VEGETATION', 'GROUND_VEHICLE', 'FAÇADE', 'WIRE', 'GARDEN_FURNITURE', 'CONCRETE', 'ROOF', 'GRAVEL', 'SOIL', 'PRIMEAIR_PATTERN', 'SNOW']


class SegmentationClass:
    BACKGROUND = 255

    def values():
        # return [1]
        return list(range(len(proto)))


def get_segmentation_annotations(segmentation_mask, DEBUG=True):
    hw = segmentation_mask.shape[:2]
    # print(hw)
    # segmentation_mask = segmentation_mask.reshape(hw)
    polygons = []

    for segtype in SegmentationClass.values():
        seg_type_name = proto[segtype]
        if segtype == SegmentationClass.BACKGROUND:
            continue
        temp_img = np.zeros(hw)
        seg_class_mask_over_seg_img = np.where(segmentation_mask==segtype)
        if np.any(seg_class_mask_over_seg_img):
            temp_img[seg_class_mask_over_seg_img] = 1
            contours, _ = cv2.findContours(temp_img.astype(np.uint8), cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
            if len(contours) < 1:
                continue
            has_relevant_contour = False
            # print(len(contours))
            for contour in contours:
                if cv2.contourArea(contour) < 2:
                    continue
                has_relevant_contour = True
                polygons.append((contour, seg_type_name))

            # canvas = np.zeros_like(temp_img)
            # print(canvas)
            # for i in range(len(contour)):
            #     cv2.drawContours(canvas , [contours[i]], -1, 1, 10)
            #     plt.imshow(canvas)
            #     plt.show()

            if DEBUG and has_relevant_contour:
                fig = plt.figure()
                fig.suptitle(seg_type_name)
                plt.imshow(temp_img)
                plt.show()
    # print(len(polygons))
    return polygons

def get_segmentation_dict(segmentation_mask, img_id="0", starting_annotation_indx=0, DEBUG=True):
    annotations = []
    for indx, (contour, seg_type) in enumerate(get_segmentation_annotations(segmentation_mask, DEBUG=DEBUG)):
        segmentation = contour.ravel().tolist()
        annotations.append({
            "segmentation": segmentation,
            "area": cv2.contourArea(contour),
            "image_id": img_id,
            "category_id": seg_type,
            "id": starting_annotation_indx + indx
        })

        break
    return annotations


img = cv2.imread('mask/0b23fb62b2624c7588da634875907631-1623259906500003313.png',0)
dict1 = get_segmentation_dict(img)
# print(dict1)
# seg_class_mask_over_seg_img = np.where(img==1)
# print(seg_class_mask_over_seg_img)
