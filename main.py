#
# Author: Frank Sepulveda
# Email: socieboy@gmail.com
#

import sys
import gi
sys.path.append(".")
import Source 
import Output 
gi.require_version('Gst', '1.0')
gi.require_version("GstApp", "1.0")
from gi.repository import Gst

# Gst.debug_set_active(True)
# Gst.debug_set_default_threshold(4)
# GObject.threads_init()
Gst.init(None)

def main():

    _input = Source.Source(1)
    _output = Output.Output('rtmp://media.streamit.live/LiveApp/test')
    
    while True:
        img = _input.capture()
    # while not sink.is_eos():
        # pass
    # loop = GObject.MainLoop()
    # bus = pipeline.get_bus()
    # 

    # pipeline.set_state(Gst.State.PLAYING)

    # Cleanup
    # pipeline.set_state(Gst.State.NULL)

if __name__ == "__main__":
    sys.exit(main())