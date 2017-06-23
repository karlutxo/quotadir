# -*- coding: utf-8 -*-
import os
import time
import shutil


def translate_size(size):
    if size.isdigit():
        size_in_bytes = int(size)
    else:
        if size.endswith('K'):
            size_in_bytes = int(size.replace('K','')) * 1024
        if size.endswith('KB'):
            size_in_bytes = int(size.replace('KB','')) * 1024
        if size.endswith('M'):
            size_in_bytes = int(size.replace('M', '')) * 1024 * 1024
        if size.endswith('MB'):
            size_in_bytes = int(size.replace('MB', '')) * 1024 * 1024
        if size.endswith('G'):
            size_in_bytes = int(size.replace('G', '')) * 1024 * 1024 * 1024
        if size.endswith('GB'):
            size_in_bytes = int(size.replace('GB', '')) * 1024 * 1024 * 1024
        if size.endswith('T'):
            size_in_bytes = int(size.replace('T', '')) * 1024 * 1024 * 1024 * 1024
        if size.endswith('TB'):
            size_in_bytes = int(size.replace('TB', '')) * 1024 * 1024 * 1024 * 1024
    return size_in_bytes


def get_size(start_path = '.'):
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
   global verbose

   verbose = True
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
#      elif opt in ("-v", "--verbose"):
#         verbose = True

if __name__ == "__main__":
   main(sys.argv[1:])

current_size = int(get_size(dir))
print 'checking ', dir,  '  Quota: ', max_size, ' (', translate_size(max_size), ') bytes  ', '  used: ' , current_size
all_subdirs = [os.path.join(dir, d) for d in os.listdir(dir) if os.path.isdir(os.path.join(dir, d))]
if verbose:
    for h in all_subdirs:
        print h, '  ', get_size(h), '  ', time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(os.stat(h).st_mtime))

while current_size > translate_size(max_size):
    oldest_subdir = min(all_subdirs, key=os.path.getmtime)
    print 'deleting ' , oldest_subdir
    shutil.rmtree(oldest_subdir)
    current_size = int(get_size(dir))
    print 'checking ', dir,  '  Quota: ', max_size, ' (', translate_size(max_size), ') bytes  ', '  used: ' , current_size
    all_subdirs = [os.path.join(dir, d) for d in os.listdir(dir) if os.path.isdir(os.path.join(dir, d))]

