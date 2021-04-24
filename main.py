#
# Author: Frank Sepulveda
# Email: socieboy@gmail.com
#

import sys
import gi
sys.path.append(".")
from Source import Source 
from Output import Output 
gi.require_version('Gst', '1.0')
gi.require_version("GstApp", "1.0")
from gi.repository import Gst

# Gst.debug_set_active(True)
# Gst.debug_set_default_threshold(4)
# GObject.threads_init()
Gst.init(None)

def main():

    _input = Source(0)
    # _output = Output.Output('rtmp://media.streamit.live/LiveApp/test')
    
    img = _input.capture()

        # _.output.Render(img)

    # _input.close()
        # if not _input.IsStreaming() or not output.IsStreaming():
            # break

if __name__ == "__main__":
    sys.exit(main())