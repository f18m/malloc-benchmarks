#!/usr/bin/python
"""Generate benchmarking result figures
"""
import sys
import os
import pylab
import json
import collections

#Benchmark = collections.namedtuple('Benchmark', ['implementation', 'threads', 'time_per_iteration'], verbose=False)
BenchmarkPoint = collections.namedtuple('BenchmarkPoint', ['threads', 'time_per_iteration'], verbose=False)
filled_markers = ('o', 'v', '^', '<', '>', '8', 's', 'p', '*', 'h', 'H', 'D', 'd', 'P', 'X')

def plot_graphs(outfilename, benchmark_dict):
    """Plot graphs for functions
    Make scatter plots for the functions and their variants.
    """
    pylab.clf()
    pylab.xlabel('Number of threads')
    pylab.ylabel('CPU cycles per malloc op')          # bench-malloc-thread uses RDTSC counter for reporting time

    nmarker=0
    for impl_name in benchmark_dict.keys():
        current_bm = benchmark_dict[impl_name]
        
        # add a line plot
        X = [ x.threads for x in current_bm ]
        Y = [ y.time_per_iteration for y in current_bm ]
        lines = pylab.plot(X, Y, '-' + filled_markers[nmarker], label=impl_name)
        
        pylab.xlim(0, max(X)+1)
        pylab.setp(lines, 'color', 'r')
        nmarker=nmarker+1

    print("Writing plot into '%s'" % outfilename)
    pylab.legend(loc='upper left')
    pylab.savefig(outfilename)
    pylab.show()


def main(args):
    """Program Entry Point
    """
    if len(args) < 2:
        print('Usage: %s <image-output-file> <file1> <file2> ...' % sys.argv[0])
        sys.exit(os.EX_USAGE)

    bm = {}
    for filename in args[1:]:
        with open(filename, 'r') as benchfile:
            bench_list = json.load(benchfile)
            #print json.dumps(bench_list, sort_keys=True, indent=4, separators=(',', ': '))
            
            bm[filename] = []
            for bench in bench_list:
                #bm[filename] = Benchmark(filename, bench['functions']['malloc']['']['threads'], bench['functions']['malloc']['']['time_per_iteration'])
                bm[filename].append(BenchmarkPoint(bench['functions']['malloc']['']['threads'], bench['functions']['malloc']['']['time_per_iteration']))
            
            print('Found {} data points in {}...'.format(len(bm[filename]), filename))
            
    plot_graphs(args[0], bm)

if __name__ == '__main__':
    main(sys.argv[1:])


