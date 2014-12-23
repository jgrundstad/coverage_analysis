from __future__ import division
import argparse
from collections import defaultdict
import sys



def scan_file(filename, window):
  '''
  Report average coverage per '-w' bp window over the provided BEDGRAPH file
  '''
  id = filename.split('_')[0]
  IDS.append(id)
  fh = open(filename, 'r')
  len_accum = 0
  cov_accum = 0
  window_len = 0
  window_num = 1
  line_count = 0
  print >>sys.stderr, "File: " + filename
  sys.stderr.write('"." = 1M lines processed: ')
  for line in fh:
    line_count += 1
    if line_count % 1000000 == 0:
      sys.stderr.write('.')
    line = line.strip()
    (chr, start, stop, cov) = line.split()
    len = int(stop) - int(start)
    for i in range(0, len):
      len_accum += 1
      cov_accum += int(cov)
      window_len += 1
      if len_accum % window == 0:
        T[window_num][id] = "%.4f" % (cov_accum / window)
        window_num += 1
        cov_accum = 0
        window_len = 0
  T[window_num][id] = "%.4f" % (cov_accum / window_len)
  sys.stderr.write('\n')

        

def print_table():
  '''
  print output in table format to provide easy charting
  '''
  for id in IDS:
    sys.stdout.write("\t" + id)
  sys.stdout.write("\n")
  for window_num in T:
    sys.stdout.write(str(window_num))
    for id in IDS:
      sys.stdout.write('\t' + str(T[window_num][id]))
    print ''


def main():
  parser = argparse.ArgumentParser(
      description="create table of coverage data for list of covWhist " + \
          "files over a given window size")
  parser.add_argument('files', metavar='F', type=str, nargs='+',
      help='A list of .covWhist files')
  parser.add_argument('-w', action='store', required=True, dest='window',
      type=int,
      help='Non-overlapping window size for averaging coverage')
  args = parser.parse_args()


  global T 
  T = defaultdict(lambda: defaultdict(str))
  global IDS
  IDS = []

  for filename in args.files:
    scan_file(filename, args.window)

  print_table()


if __name__ == '__main__':
  main()
