import gi
gi.require_version('Gst', '1.0')
gi.require_version("GstApp", "1.0")
from gi.repository import Gst

class Source:

    def __init__(self, source):
        self.source = source
        self.mAppSink = None
        self.mBus = None
        self.mPipeline = None
        self.isStreaming = False
        print("INFO -- Creating Gst Source")
        self.init()
        print("INFO -- Created Gst Source")


    def init(self):

        # Create pipeline from string
        pipeStr = "nvarguscamerasrc name=camera sensor-id=" + str(self.source) + " ! " \
                 "video/x-raw(memory:NVMM), width=(int)1920, height=(int)1080, framerate=30/1, format=(string)NV12 ! " \
                 "nvvidconv flip-method=0 ! " \
                 "video/x-raw ! " \
                 "appsink name=appsink"

        print("INFO -- Camera pipeline string:\n\n" + pipeStr + "\n")
        self.mPipeline = Gst.parse_launch(pipeStr)

        if not self.mPipeline:
            print('ERROR -- Camera failed to create pipeline')
            return False
            
        # Create bus
        self.mBus = self.mPipeline.get_bus()
        if not self.mBus:
            print('ERROR -- Camera failed to retrieve GstBus from pipeline')
            return False
        # self.mBus.add_signal_watch()
        # self.mBus.connect ("message", bus_call, NULL)
        
        # Create appSink element
        self.mAppSink = self.mPipeline.get_by_name("appsink")
        if not self.mAppSink:
            print('ERROR -- Camera failed to retrieve AppSink element from pipeline')
            return False

        # Register signal callbacks
        self.mAppSink.connect("eos", self.__onEOS)
        self.mAppSink.connect("new_preroll", self.__onPreroll)
        self.mAppSink.connect("new_sample", self.__onBuffer)

        return True

    def capture(self):
        if not self.isStreaming:
            if not self.open():
                return False
            
    def open(self):
        if self.isStreaming:
            return True
        print("Camera-- starting pipeline, transitioning to GST_STATE_PLAYING")
        result = self.mPipeline.set_state(Gst.State.PLAYING)
        self.isStreaming = True


    def __onEOS(self, appSink, userData = None):
        print("Camera -- end of stream (EOS)")

    def __onPreroll(self, appSink, userData = None):
        print("Camera -- onPreroll")
        return Gst.FlowReturn.OK

    def __onBuffer(self, appSink, userData = None):
        print("Camera -- onBuffer")
        print(appSink)
        print(userData)
        if not userData:
            return Gst.FlowReturn.OK

        self.__checkBuffer()

        return Gst.FlowReturn.OK
    
    def __checkBuffer(self):
        pring("Camera -- Checking buffer")
        if not self.mAppSink:
            return

        gstSample = self.mAppSink.pull_sample()
        if not gstSample:
            print("Camera -- gst_app_sink_pull_sample() returned NULL...")
            return
        
        (result, map) = self.mBus.map(Gst.MapFlags.READ)
        assert result

        # gstData = map.data
        # gstSize = map.maxsize
	
	    # if not gstData:
		#     print("Camera -- gst_buffer_map had NULL data pointer...")
		#     return

        # if map.maxsize > map.size:
            # print("Camera -- map buffer size was less than max size")

        # gstCaps = gstSample.caps

        # gstBuffer = Gst.gstSam(gstSample);

    # def __checkMsgBus()
    	# while(True):
		    # msg = gst_bus_pop(self.mBus.get)

		# if not msg:
		    # break

		# gst_message_print(mBus, msg, this);
		# gst_message_unref(msg);