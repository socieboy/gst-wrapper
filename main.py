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

    _input = Source.Source(0)
    _output = Output.Output('rtmp://media.streamit.live/LiveApp/test')
    
    while True:
        img = _input.Capture()

        # _.output.Render(img)

        # if not _input.IsStreaming() or not output.IsStreaming():
            # break

if __name__ == "__main__":
    sys.exit(main())