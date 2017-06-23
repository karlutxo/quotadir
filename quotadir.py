# -*- coding: utf-8 -*-
import os
import time
import shutil
import sys, argparse


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


dir = ''
max_size = 1073741824  # 1 GB


verbose = False
force = False

parser = argparse.ArgumentParser(description='Caps the size of a directory by means of deleting the older subdirs',epilog='v. 1.0 Jun17 by Carlos Jimenez')
parser.add_argument("path", help="path of the directory to check")
parser.add_argument("size", help="Size of the quota. Use KB, MB, GB or TB")
parser.add_argument("-v", "--verbose", help="increase output verbosity",  action="store_true")
parser.add_argument("-f", "--force", help="do not prompt before deleting",  action="store_true")
args = parser.parse_args()

if args.verbose:
   verbose = True

if args.force:
   force = True

dir = args.path
max_size = args.size

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

