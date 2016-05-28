from __future__ import print_function
from __future__ import division

from skvideo.io import VideoCapture
import sys

filename = sys.argv[1]
cap = VideoCapture(filename)

frame_num = 0

cap.open()
while True:
    retval, image = cap.read()
    if not retval:
        break

    print("frame %d" % (frame_num))
    frame_num += 1

cap.release()
print("done")
