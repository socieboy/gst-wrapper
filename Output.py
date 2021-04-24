import gi
gi.require_version('Gst', '1.0')
gi.require_version("GstApp", "1.0")
from gi.repository import Gst

class Output():

    def __init__(self, dest):
        self.dest = dest
        self.mAppSrc = None
        self.mBus = None
        self.mBufferCaps = None
        self.mPipeline = None
        self.mNeedData = None
        self.mOutputPort = 0
        print("INFO -- Creating Gst Output")
        self.start()
        print("INFO -- Created Gst Output")
    
    def start(self):
        # Create pipeline from string
        pipeStr = "appsrc name=appsrc is-live=true do-timestamp=true format=3 ! " \
                  "omxh264enc bitrate=4000000 ! " \
                  "video/x-h264 ! " \
                  "flvmux streamable=true ! " \
                  "queue ! " \
                  "rtmpsink location=" + self.dest

        print("INFO -- Output pipeline string:\n\n" + pipeStr + "\n")
        self.mPipeline = Gst.parse_launch(pipeStr)

        if not self.mPipeline:
            print('ERROR -- Output failed to create pipeline')
            return False

        # Create bus
        self.mBus = self.mPipeline.get_bus()
        if not self.mBus:
            print('ERROR -- Output failed to retrieve GstBus from pipeline')
            return False
        # self.mBus.add_signal_watch()
        # self.mBus.connect ("message", bus_call, NULL)

        # Create appSink element
        self.mAppSrc = self.mPipeline.get_by_name("appsrc")
        if not self.mAppSrc:
            print('ERROR -- Output failed to retrieve AppSrc element from pipeline')
            return False

        # Register signal callbacks
        self.mAppSrc.connect("need-data", self.__onNeedData)
        self.mAppSrc.connect("enough-data", self.__onEnoughData)

        return True
    
    def __onNeedData(self, pipeline, size, userData):
        print("Output -- appsrc requesting data (" + size + " bytes)")
        if not userData:
            return
        self.mNeedData = True

    def __onEnoughData(self, pipeline, userData):
        print("Output -- appsrc signalling enough data")
        if not userData:
            return
        self.mNeedData = True