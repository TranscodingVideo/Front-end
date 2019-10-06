import os 
import mimetypes
import arrow

#timeformat takes 
def timeformat(time_str):
    time = arrow.get(time_str)
    return time.humanize()

def file_type(object_key):
    # creates a tuple from the whole file name
    # [0] file name
    # [1] file extention
    file_info = os.path.splitext(object_key)
    file_ext = file_info[1]
    try:
        return mimetypes.types_map[file_ext]
    except KeyError():
        return 'Unknown'