import inspect
import sys
import os
import hashlib
import datetime

def set_doc_date_0(doc):
  """Sets the document date to unix epoch start."""
  # 1969-12-31 19:00:00
  time_tuple = (1969, 12, 31, 19, 00, 00)
  zero = datetime.datetime(*time_tuple)
  doc.set_creation_date(zero)

def calculate_hash_of_file(full_path):
  """Finds md5 hash of a file given an abs path, reading in whole file."""
  hash_md5 = hashlib.md5()
  with open(full_path, "rb") as f:
    for chunk in iter(lambda: f.read(4096), b""):
      hash_md5.update(chunk)
  return hash_md5.hexdigest()

def relative_path_to(place):
  """Finds Relative Path to a place

  Works by getting the file of the caller module, then joining the directory
  of that absolute path and the place in the argument.
  """
  caller_file = inspect.getfile(sys._getframe(1))
  return os.path.join(os.path.dirname(os.path.abspath(caller_file)), place)
