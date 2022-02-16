from argparse import ArgumentParser
import os
import sys
import glob

sys.path.append(os.path.abspath('./pytorch_yolov3'))
import detect_image

sys.path.append(os.path.abspath('../common'))
from cdd import convert_darknettxt_dataset

global opts
opts = {}

def parseOptions():
    argparser = ArgumentParser()
    argparser.add_argument('--imgdir',  help=':specify image file') # use action='store_true' as flag
    args = argparser.parse_args()
    if args.imgdir: opts.update({'imgdir':args.imgdir})

def main(imgdir):
    args_config = "./yolov3_custom.yaml"
    args_weights = "./train_output/yolov3_final.pth"
    args_gpu_id = 0
    args_output = "./output"
    detector = detect_image.Detector(args_config, args_weights, args_gpu_id)

    label_file = "./custom_classes.txt"
    labels = convert_darknettxt_dataset.csvread(label_file)
    # print (f"%s %s" % (labels[0], labels[1]))

    img_files = list(glob.glob(f'{imgdir}/*/*/*.jpg'))
    for image in img_files:
        detections, img_paths = detector.detect_from_path(image)
        for detection, img_path in zip(detections, img_paths):
            check = [False, False]
            for box in detection:
                print(
                    f"{box['class_name']} {box['confidence']:.0%} "
                    f"({box['x1']:.0f}, {box['y1']:.0f}, {box['x2']:.0f}, {box['y2']:.0f})"
                )
                if box['class_name'] == labels[0][0]:
                    check[0] = True
                if box['class_name'] == labels[1][0]:
                    check[1] = True
            if (check[0] == True and check[1] == True):
                print (f"label0 and label1 are available in {img_path}")
                # if not os.path.isdir(args_output):
                #     os.makedirs(args_output)
                # img = detect_image.Image.open(img_path)
                # detector.draw_boxes(img, detection)
                # img.save(args_output + "/" + detect_image.Path(img_path).name)
            else:
                print (f"label0 or label1 is not available in {img_path}")
                os.remove(img_path)

if __name__ == "__main__":
    parseOptions()
    if ('imgdir' in opts.keys()):
        main(opts['imgdir'])
