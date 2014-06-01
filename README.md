scikit-video
============

Video Processing SciKit

*Currently in PLANNING STAGE.*

Video processing algorithms, including IO, quality metrics, temporal filtering, motion/object detection, motion estimation...

This is intended as a companion to scikit-image, containing all the algorithms which deal with *video*.  There is a certain degree of overlap between image and video algorithms, for example a PSNR quality metric could be applied to pairs of images or pairs of video frames just as well.  However, other algorithms are video-specific, for example a temporal denoise.  This is the future home of the video-specific algorithms, as well as some of the algorithms which are not strictly video specific but are usually seen in a video context.

This also has some overlap with OpenCV.  Roughly, the algorithms implemented here would be easier to hack on, and more research-oriented.  Rather than building on top of a C/C++ framework, this will stay Python all the way, using whichever combinaiton of Numba/Theano/etc seems best for performance.  This should add flexibility and better future ability to use GPU compute.

The project milestones are roughly:

- Add skeleton project from scikit-example
- Add video IO by wrapping ffmpeg/libav (similar to kanryu/pipeffmpeg)
- Add video metrics (from aizvorski/video-quality)
- More contributions roll in :)
