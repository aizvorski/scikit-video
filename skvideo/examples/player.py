from skvideo.io import VideoCapture

import sys
import matplotlib.pyplot as plt
import matplotlib.animation as animation

filename = sys.argv[1]
cap = VideoCapture(filename)
print str(cap.get_info())


cap.open()
retval, image = cap.read()

plt_fig = plt.figure()
plt_image = plt.imshow(image)

frame_num = 0

def updatefig(*args):
    global cap, frame_num

    retval, image = cap.read()

    if not retval:
        print "done"
        sys.exit()

    print "frame %d" % (frame_num)
    frame_num += 1

    plt_image.set_array(image)
    return plt_image,

plt_ani = animation.FuncAnimation(plt_fig, updatefig, interval=33, blit=True)
plt.show()

