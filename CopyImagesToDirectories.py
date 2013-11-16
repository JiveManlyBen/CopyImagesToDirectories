from PIL import Image
from PIL.ExifTags import TAGS
import os
import filecmp
import sys
import shutil
import time

def get_example_text():
	if os.path.sep == "\\":
		return "Example: python CopyImagesToDirectories.py c:\\input\\ c:\\pics\\"
	else:
		return "Example: python CopyImagesToDirectories.py /usr/local/input/ /usr/local/pics/"

def add_trailing_separator(file_path):
	if file_path[-1:] != os.path.sep:
		return file_path + os.path.sep
	else:
		return file_path

def get_file_system_time(file_path):
	return time.localtime(os.path.getmtime(file_path))

def get_exif_time(file_path):
    ret = {}
    try:
		i = Image.open(file_path)
		info = i._getexif()
		for tag, value in info.items():
			if TAGS.get(tag, tag) == "DateTimeOriginal":
				if value is not None:
					return time.strptime(value, '%Y:%m:%d %H:%M:%S')
				else:
					return None
    except IOError, e:
        return None

try:
	in_path = add_trailing_separator(sys.argv[1])
	out_path = add_trailing_separator(sys.argv[2])
except IndexError, e:
	print "required input and output directories not supplied: " + str(e)
	print "\n" + get_example_text()
	exit()

message = ""
copied_image_count = 0
failed_image_count = 0
try:
	for f in os.listdir(in_path):
		if os.path.isfile(os.path.join(in_path, f)):
			if f.lower().endswith(".jpg") or f.lower().endswith(".cr2") or f.lower().endswith(".mov"):
				image_time = get_exif_time(in_path + f)
				if image_time is None:
					image_time = get_file_system_time(in_path + f)
				y_path = time.strftime("%Y", image_time)
				m_path = time.strftime("%Y" + os.path.sep +"%Y_%m", image_time)
				d_path = time.strftime("%Y" + os.path.sep +"%Y_%m" + os.path.sep + "%Y_%m_%d", image_time)
				f_path = os.path.join(os.path.join(out_path, d_path), f)
				if not os.path.exists(os.path.join(out_path, d_path)):
					if os.path.exists(os.path.join(out_path, m_path)):
						os.makedirs(os.path.join(out_path, d_path))
					else:
						if os.path.exists(os.path.join(out_path, y_path)):
							os.makedirs(os.path.join(out_path, m_path))
							os.makedirs(os.path.join(out_path, d_path))
						else:
							os.makedirs(os.path.join(out_path, y_path))
							os.makedirs(os.path.join(out_path, m_path))
							os.makedirs(os.path.join(out_path, d_path))

				if (not os.path.isfile(f_path)):
					print "copying " + os.path.join(in_path, f)
					shutil.copy2(os.path.join(in_path, f), f_path)
					copied_image_count += 1
				elif not filecmp.cmp(os.path.join(in_path, f), f_path):
					print "warning: file mismatch for \"" + f_path + "\""
					failed_image_count += 1
except (IOError, OSError), e:
	message = str(e)
finally:
	if len(message) > 0:
		message = "\n" + message
	if failed_image_count > 0:
		message = " (with " + str(failed_image_count) + " errors)" + message
	message = "Copied " + str(copied_image_count) + " new images from \"" + in_path + "\" to \"" + out_path + "\"" + message
	print message