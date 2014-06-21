from skvideo.io import VideoCapture

import sys

filename = sys.argv[1]
cap = VideoCapture(filename)
print str(cap.get_info())


cap.open()
retval, image = cap.read()



frame_num = 0


import numpy
import pygame

while True:
    retval, image = cap.read()

    if not retval:
        print "done"
        sys.exit()

    surface = pygame.surfarray.make_surface(image)

    surface = pygame.Surface((100, 100))
    numpy_surface = numpy.frombuffer(surface.get_buffer())
    numpy_surface[...] = numpy.frombuffer(image)
    del numpy_surface

    screen = pygame.display.set_mode((100, 100))
    screen.blit(surface, (0, 0))
    pygame.display.flip()

