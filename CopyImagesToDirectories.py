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
	
try:
	in_path = sys.argv[1]
	out_path = sys.argv[2]
except IndexError, e:
	print "required input and output directories not supplied: " + str(e)
	print "\n" + get_example_text()
	exit()
try:
	not_copied = False
        for f in os.listdir(in_path):
                if os.path.isfile(os.path.join(in_path, f)):
			if f.lower().endswith(".jpg") or f.lower().endswith(".cr2") or f.lower().endswith(".mov"):
				y_path = time.strftime("%Y", time.localtime(os.path.getmtime(in_path + f)))
				m_path = time.strftime("%Y" + os.path.sep +"%Y_%m", time.localtime(os.path.getmtime(in_path + f)))
				d_path = time.strftime("%Y" + os.path.sep +"%Y_%m" + os.path.sep + "%Y_%m_%d", time.localtime(os.path.getmtime(in_path + f)))
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
				elif not filecmp.cmp(os.path.join(in_path, f), f_path):
					print "warning: file mismatch for \"" + f_path + "\""
					not_copied = True
	print "Copied new images from \"" + in_path + "\" to \"" + out_path + "\""
	if not_copied:
		print "with errors"
except OSError, e:
        print e
