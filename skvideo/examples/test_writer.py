from __future__ import print_function
from __future__ import division

from skvideo.io import VideoWriter
import sys
import numpy

w, h = 640, 480

filename = sys.argv[1]
wr = VideoWriter(filename, frameSize=(w, h))

x = numpy.linspace(0, 2 * numpy.pi, w)
y = numpy.linspace(0, 2 * numpy.pi, h).reshape(-1, 1)

def f(x, y):
    return numpy.sin(x) + numpy.cos(y)

frame_num = 0

wr.open()
while True:
    x += numpy.pi / 15.
    y += numpy.pi / 20.
    image = numpy.zeros((h, w, 3))
    image[:,:,0] = (f(x, y) + 2)* 64
    image[:,:,1] = (f(x+numpy.pi/2, y+numpy.pi/2) + 2)* 64

    wr.write(image)

    print("frame %d" % (frame_num))
    frame_num += 1
    if frame_num > 300:
        break

wr.release()
print("done")
