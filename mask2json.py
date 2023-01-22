# https://github.com/chrise96/image-to-coco-json-converter
import glob

from create_annotations import *

proto = ['WATER', 'ASPHALT', 'GRASS', 'HUMAN', 'ANIMAL', 'HIGH_VEGETATION', 'GROUND_VEHICLE', 'FAÇADE', 'WIRE', 'GARDEN_FURNITURE', 'CONCRETE', 'ROOF', 'GRAVEL', 'SOIL', 'PRIMEAIR_PATTERN', 'SNOW']

category_ids = {i:idx for idx,i in enumerate(proto)}
# Define which colors match which categories in the images

category_colors = {str(i):i for i in range(len(proto))}


# Get "images" and "annotations" info 
def images_annotations_info(maskpath):
    # This id will be automatically increased as we go
    annotation_id = 0
    image_id = 0
    annotations = []
    images = []
    
    for mask_image in glob.glob(maskpath + "/*.png"):

        original_file_name = mask_image.replace('mask', 'image')
        
        mask_image_open = Image.open(mask_image)
        w, h = mask_image_open.size

        image = create_image_annotation(original_file_name, w, h, image_id)
        images.append(image)
        
        sub_masks = create_sub_masks(mask_image_open, w, h)
        
        for color, sub_mask in sub_masks.items():
            if color == '255': continue

            category_id = category_colors[color]
            polygons, segmentations = create_sub_mask_annotation(sub_mask)
            multi_poly = MultiPolygon(polygons)                        
            annotation = create_annotation_format(multi_poly, segmentations, image_id, category_id, annotation_id)
            annotations.append(annotation)
            annotation_id += 1

            # for i in range(len(polygons)):
            #     # Cleaner to recalculate this variable
            #     segmentation = [np.array(polygons[i].exterior.coords).ravel().tolist()]
                
            #     annotation = create_annotation_format(polygons[i], segmentation, image_id, category_id, annotation_id)
                
            #     annotations.append(annotation)
            #     annotation_id += 1

        image_id += 1
    return images, annotations, annotation_id

if __name__ == "__main__":
    # Get the standard COCO JSON format
    coco_format = get_coco_json_format()
    
    mask_path = 'mask'
        
    coco_format["categories"] = create_category_annotation(category_ids)
    
    coco_format["images"], coco_format["annotations"], annotation_cnt = images_annotations_info(mask_path)

    with open("test.json","w") as outfile:
        json.dump(coco_format, outfile)
    
    print("Created %d annotations for images in folder: %s" % (annotation_cnt, mask_path))
# images_annotations_info('mask')