import numpy
import subprocess
import json

class VideoCapture:
    """
    Read video using avconv or ffmpeg in a subprocess.

    The API is modelled after cv2.VideoCapture, and in many cases is a drop-in replacement.
    """

    def __init__(self, filename=None, frameSize=None):
        self.filename = filename
        # TODO find either avconv or ffmpeg, remember which one we found
        self.convert_command = "avconv"
        self.probe_command = "avprobe"
        self.proc = None

        if frameSize:
            self.do_resize = True
            self.width, self.height = frameSize
        else:
            self.do_resize = False

        if self.filename:
            self.info = self.get_info()
            if len(self.info["streams"]) == 0:
                raise ValueError("No streams found")
            if self.info["streams"][0]["codec_type"] != "video":
                raise ValueError("No video stream found")
            self.src_width = self.info["streams"][0]["width"]
            self.src_height = self.info["streams"][0]["height"]
            if not self.do_resize:
                self.width = self.src_width
                self.height = self.src_height

            self.depth = 3 # TODO other depths
            # print "Found video: %d x %d" %(self.width, self.height)
            self.open()

    def open(self):
        # TODO decide what is best behavior, reopen or leave as it if previously opened
        if self.isOpened():
            self.release()
        cmd = [self.convert_command, '-loglevel', 'error', '-i', self.filename]
        if self.do_resize:
            cmd += ['-vf', 'scale=%d:%d' %(self.width, self.height)]
        cmd += ['-f', 'rawvideo', '-pix_fmt', 'rgb24', '-']
        self.proc = subprocess.Popen(cmd, stdout=subprocess.PIPE)
        self.buf = ""

    def isOpened(self):
        return (self.proc != None)

    def read(self):
        retval = True

        nbytes = self.width * self.height * self.depth

        while len(self.buf) < nbytes:

            # Could poll here, but return code never seems to be set before we fail at reading anyway
            # self.proc.poll()

            if self.proc.returncode != None:
                if self.proc.returncode < 0:
                    raise ValueError("Command exited with return code %d" % (self.proc.returncode)) # TODO subprocess.CalledProcessError?
                else:
                    return False, None

            buf = self.proc.stdout.read( nbytes - len(self.buf) )
            # print "Read %d" % (len(buf))

            # Reading no data seems to be a reliable end-of-file indicator; return code is not.
            if len(buf) == 0:
                break

            self.buf += buf
        
        if len(self.buf) < nbytes:
            # We didn't get any data, assume end-of-file
            if len(self.buf) == 0:
                return False, None
            # We got some data but not enough, this is an error
            else:
                raise ValueError("Not enough data at end of file, expected %d bytes, read %d" % (nbytes, len(self.buf)))

        image = numpy.fromstring(self.buf[:nbytes], dtype=numpy.uint8).reshape((self.height, self.width, self.depth))

        # If there is data left over, move it to beginning of buffer for next frame
        if len(self.buf) > nbytes:
            self.buf = self.buf[nbytes:] # TODO this is a relatively slow operation, optimize
        # Otherwise just forget the buffer
        else:
            self.buf = ""

        return retval, image

    def seek(self, time):
        raise NotImplementedError()

    def release(self):
        self.proc.kill()
        self.proc = None
        self.buf = None

    def get(self, propId):
        # CV_CAP_PROP_FRAME_COUNT
        raise NotImplementedError()

    def set(self, propId, value):
        raise NotImplementedError()

    def get_info(self):
        # NOTE requires a fairly recent avprobe/ffprobe, older versions don't have -of json and only produce INI-like output
        # TODO parse old INI-like output
        cmd = [self.probe_command] + "-loglevel error -of json -show_format -show_streams".split() + [self.filename]
        output = subprocess.check_output(cmd)
        info = json.loads(output)
        return info

class VideoWriter:
    def __init__(self, filename, fourcc='XVID', fps=30, frameSize=(640, 480), isColor=True):
        self.filename = filename
        self.convert_command = "avconv"

        self.fourcc = fourcc
        self.fps = fps
        self.width, self.height = frameSize
        self.depth = 3 # TODO other depths

        if not isColor:
            raise NotImplementedError()


    def open(self):
        cmd = [self.convert_command, '-loglevel', 'error', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', '%dx%d' %(self.width, self.height), '-r', str(self.fps), '-i', '-']
        codecs_map = {
            'XVID': 'mpeg4',
            'DIVX': 'mpeg4',
            'H264': 'libx264',
            'MJPG': 'mjpeg',
        }
        if self.fourcc in codecs_map:
            vcodec = codecs_map[self.fourcc]
        else:
            vcodec = self.fourcc
        cmd += ['-vcodec', vcodec]
        cmd += [self.filename]
        self.proc = subprocess.Popen(cmd, stdin=subprocess.PIPE)

    def isOpened(self):
        return (self.proc != None)

    def write(self, image):
        if image.shape[0] != self.height or image.shape[1] != self.width or image.shape[2] != self.depth:
            raise ValueError('Image dimensions do not match')
        self.proc.stdin.write( image.astype(numpy.uint8).tostring() )

    def release(self):
        self.proc.stdin.close()
        self.proc.wait()
        self.proc = None


