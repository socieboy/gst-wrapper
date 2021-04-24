#!/usr/bin/env python3

import gi, sys
gi.require_version('Gst', '1.0')
gi.require_version("GstApp", "1.0")
from gi.repository import Gst

def gst_message_print(bus, msg, source):

	_type = msg.type

	if _type == Gst.MessageType.ERROR:
		err, dbg = msg.parse_error()
		print("Camera - ERROR:", msg.src.get_name(), " ", err.message)
		if dbg:
			print("debugging info:", dbg)

	elif _type == Gst.MessageType.EOS:
		print("Camera -- gstreamer end of stream")

	elif _type == Gst.MessageType.STATE_CHANGED:
		old_state, new_state, pending_state = msg.parse_state_changed()
		print("Camera -- gstreamer state changed from \"{0:s}\" to \"{1:s}\" on \"{2:s}\"".format(Gst.Element.state_get_name(old_state), Gst.Element.state_get_name(new_state), msg.src.get_name()))

	elif _type == Gst.MessageType.STREAM_STATUS:
		print("Camara -- gstreamer stream status \"{0:s}\" on \"{1:s}\"".format(gst_print_message_status_type(msg), msg.src.get_name()))

	elif _type == Gst.MessageType.TAG:
		print('Gst.MessageType.TAG')
		taglist = msg.parse_tag()
		print(taglist)
			# //gst_tag_list_foreach(tags, gst_print_one_tag, NULL);

			# if( tags != NULL )			
				# gst_tag_list_free(tags);

	else:
		print("Camara -- \"{0:s}\" message received on \"{1:s}\"".format(Gst.MessageType.get_name(msg.type), msg.src.get_name()))
		pass
	return True


def gst_print_message_status_type(msg):
	if Gst.Message.parse_stream_status(msg).type == Gst.StreamStatusType.CREATE: return "CREATE"
	if Gst.Message.parse_stream_status(msg).type == Gst.StreamStatusType.ENTER: return "ENTER"
	if Gst.Message.parse_stream_status(msg).type == Gst.StreamStatusType.LEAVE: return "LEAVE"
	if Gst.Message.parse_stream_status(msg).type == Gst.StreamStatusType.DESTROY: return "DESTROY"
	if Gst.Message.parse_stream_status(msg).type == Gst.StreamStatusType.START: return "START"
	if Gst.Message.parse_stream_status(msg).type == Gst.StreamStatusType.PAUSE: return "PAUSE"
	if Gst.Message.parse_stream_status(msg).type == Gst.StreamStatusType.STOP: return "STOP"
	return "UNKNOWN";