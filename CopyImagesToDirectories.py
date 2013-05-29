import os
import filecmp
import sys
import shutil
import time

try:
	in_path = sys.argv[1]
	out_path = sys.argv[2]
except IndexError, e:
	print "required input and output directories not supplied " + str(e)
	exit()
try:
	not_copied = False
        for f in os.listdir(in_path):
                if os.path.isfile(os.path.join(in_path, f)):
			if f.lower().endswith(".jpg") or f.lower().endswith(".cr2"):
	                       	new_location = os.path.join(out_path, time.strftime("%Y"+os.pathsep, time.localtime(os.path.getmtime(in_path + f))))
				if not os.path.exists(new_location):
					os.makedirs(new_location)
	                       	new_location = os.path.join(new_location, time.strftime("%Y_%m_%d", time.localtime(os.path.getmtime(in_path + f))))
				if not os.path.exists(new_location):
					os.makedirs(new_location)
	                       	new_location = os.path.join(new_location, f)
				if (not os.path.isfile(new_location)):
					print "copying " + os.path.join(in_path, f)
					shutil.copy2(os.path.join(in_path, f), new_location)
				elif not filecmp.cmp(os.path.join(in_path, f), new_location):
					print "warning: file mismatch for \"" + new_location + "\""
					not_copied = True
	print "Copied new images from \"" + in_path + "\" to \"" + out_path + "\""
	if not_copied:
		print "with errors"
except OSError, e:
        print e
