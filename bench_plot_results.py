#!/usr/bin/python
"""Generates a figure that shows all benchmarking results
"""
import sys
import os
import json
import collections

import matplotlib.pyplot as plotlib

BenchmarkPoint = collections.namedtuple('BenchmarkPoint', ['threads', 'time_per_iteration'], verbose=False)
filled_markers = ('o', 'v', '^', '<', '>', '8', 's', 'p', '*', 'h', 'H', 'D', 'd', 'P', 'X')

def plot_graphs(outfilename, benchmark_dict):
    """Plots the given dictionary of benchmark results
    """
    plotlib.clf()
    plotlib.xlabel('Number of threads')
    plotlib.ylabel('CPU cycles per malloc op')          # bench-malloc-thread uses RDTSC counter for reporting time => CPU clock cycles

    nmarker=0
    max_x=[]
    max_y=[]
    for impl_name in benchmark_dict.keys():
        current_bm = benchmark_dict[impl_name]
        
        # add a line plot
        X = [ x.threads for x in current_bm ]
        Y = [ y.time_per_iteration for y in current_bm ]
        lines = plotlib.plot(X, Y, '-' + filled_markers[nmarker], label=impl_name)
        
        # remember max X/Y
        max_x.append(max(X))
        max_y.append(max(Y))
        
    plotlib.xlim(0, max(max_x)*1.1)
    plotlib.ylim(0, max(max_y)*1.3)
    plotlib.setp(lines, 'color', 'r')
    nmarker=nmarker+1

    print("Writing plot into '%s'" % outfilename)
    plotlib.legend(loc='upper left')
    plotlib.savefig(outfilename)
    plotlib.show()


def main(args):
    """Program Entry Point
    """
    if len(args) < 2:
        print('Usage: %s <image-output-file> <file1> <file2> ...' % sys.argv[0])
        sys.exit(os.EX_USAGE)

    bm = {}
    for filepath in args[1:]:
        with open(filepath, 'r') as benchfile:
            filename = os.path.basename(filepath)
            bench_list = json.load(benchfile)
            #print json.dumps(bench_list, sort_keys=True, indent=4, separators=(',', ': '))
            
            bm[filename] = []
            for bench in bench_list:
                bm[filename].append(BenchmarkPoint(bench['functions']['malloc']['']['threads'], bench['functions']['malloc']['']['time_per_iteration']))
            
            print('Found {} data points in {}...'.format(len(bm[filename]), filepath))
            
    plot_graphs(args[0], bm)

if __name__ == '__main__':
    main(sys.argv[1:])


