from __future__ import print_function
from __future__ import division

from skvideo.io import VideoCapture
from skvideo.metrics import ssim, psnr, vifp
import sys
import json

filename1, filename2 = sys.argv[1], sys.argv[2]

cap1 = VideoCapture(filename1)
cap1.open()
print(str(cap1.get_info()))

cap2 = VideoCapture(filename2)
cap2.open()
print(str(cap2.get_info()))

def rgb_to_y(img):
    return 0.299 * img[:,:,0] + 0.587 * img[:,:,1] + 0.114 * img[:,:,2]

frame_num = 0
while True:
    retval1, image1 = cap1.read()
    retval2, image2 = cap2.read()

    if not retval1 and not retval2:
        break
    elif not retval1 or not retval2:
        print("error: input files have different number of frames")
        break

    if image1.shape != image2.shape:
        print("error: input files have different resolutions")

    y_image1 = rgb_to_y(image1)
    y_image2 = rgb_to_y(image2)

    psnr_metric = psnr.psnr(image1, image2)
    ssim_metric = ssim.ssim(y_image1 / 255.0, y_image2 / 255.0)
    vifp_metric = vifp.vifp_mscale(y_image1, y_image2)

    print(json.dumps({ "frame_num":frame_num, "psnr":psnr_metric, "ssim":ssim_metric, "vifp":vifp_metric }))
    frame_num += 1

cap1.release()
cap2.release()
print("done")
