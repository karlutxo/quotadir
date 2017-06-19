# -*- coding: utf-8 -*-
import os


def get_size(start_path = '.'):
    print 'get_size: start_paht=' , start_path
    total_size = 0
    for dirpath, dirnames, filenames in os.walk(start_path):
        for f in filenames:
            fp = os.path.join(dirpath, f)
            total_size += os.path.getsize(fp)
    return total_size

import sys, getopt

dir = ''
max_size = 1073741824  # 1 GB


def main(argv):
   global dir
   global max_size
   try:
      opts, args = getopt.getopt(argv,"hd:s:",["dir=","size="])
   except getopt.GetoptError:
      print 'quota.py -d <dir> -s <size'
      sys.exit(2)
   for opt, arg in opts:
      if opt == '-h':
         print 'quota.py -d <dir> -s <size>'
         sys.exit()
      elif opt in ("-d", "--dir"):
         dir = arg
      elif opt in ("-s", "--size"):
         max_size = arg

if __name__ == "__main__":
   main(sys.argv[1:])
print 'dir is ', dir
print 'max_size is ', max_size, type(max_size)

current_size = int(get_size(dir))
print 'current size is ' , current_size, type(dir)
if int(current_size) > int(max_size):
#if 10 > 9:
        print 'hay que borrar'
else:
    print 'no hay que borrar'

print '1 ',os.listdir('/vl/vm/')
#all_subdirs = [d for d in os.listdir('/vl/vm/') if os.path.isdir(d)]
all_subdirs = [d for d in os.listdir('/vl/vm/')]


print 'subdirs ', all_subdirs
#oldest_subdir = min(all_subdirs, key=os.path.getmtime)
#print 'oldest_subdir' , oldest_subdir
print 'all_subdir' , all_subdirs