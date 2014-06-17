import numpy
import subprocess
import json

class VideoCapture:
    """
    Read video using avconv or ffmpeg in a subprocess.

    The API is modelled after cv2.VideoCapture, and in many cases is a drop-in replacement.
    """

    def __init__(self, filename=None):
        self.filename = filename
        self.info = self.get_info()
        if len(self.info["streams"]) == 0:
            raise ValueError("No streams found")
        if self.info["streams"][0]["codec_type"] != "video":
            raise ValueError("No video stream found")
        self.width = self.info["streams"][0]["width"]
        self.height = self.info["streams"][0]["height"]
        self.depth = 3 # TODO other depths
        # print "Found video: %d x %d" %(self.width, self.height)

    def open(self):
        # TODO find either avconv or ffmpeg, remember which one we found
        cmd = ["avconv", '-i', self.filename, '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-loglevel', 'error', '-']
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

        image = numpy.fromstring(self.buf[:nbytes], dtype='uint8').reshape((self.height, self.width, self.depth))

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
        raise NotImplementedError()

    def set(self, propId, value):
        raise NotImplementedError()

    def get_info(self):
        # NOTE requires a fairly recent avprobe/ffprobe, older versions don't have -of json and only produce INI-like output
        # TODO parse old INI-like output
        cmd = "avprobe -of json -show_format -show_streams -loglevel error".split() + [self.filename]
        output = subprocess.check_output(cmd)
        info = json.loads(output)
        return info

class VideoWriter:
    def __init__(self, filename, fourcc='XVID', fps=30, frameSize=None, isColor=True):
        raise NotImplementedError()

    def open(self):
        raise NotImplementedError()

    def isOpened(self):
        raise NotImplementedError()

    def write(self, image):
        raise NotImplementedError()

    def release(self):
        raise NotImplementedError()


