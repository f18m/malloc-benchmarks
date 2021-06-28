#!/usr/bin/python3
"""Generates a figure that shows all benchmarking results
"""
import sys
import os
import json

import matplotlib.pyplot as plotlib

filled_markers = ('o', 'v', '^', '<', '>', '8', 's', 'p', '*', 'h', 'H', 'D', 'd', 'P', 'X')
colours = ('r', 'g', 'b', 'black', 'yellow', 'purple')

def plot_graphs(outfilename, benchmark_dict):
    """Plots the given dictionary of benchmark results
    """
    # print("benchmark_dict = {}".format(benchmark_dict))

    # any one of the data sets--just to grab some subtitle data that is common to all the data sets
    a_key = list(benchmark_dict.keys())[0]
    data_dict = benchmark_dict[a_key][0]
    # print("data_dict = {}".format(data_dict))

    plotlib.clf()
    # main figure title
    plotlib.suptitle("Malloc speed tests (tested w/glibc's `benchtests/bench-malloc-thread.c`)")
    # figure subtitle
    plotlib.title("num bytes per malloc: min = {}; max = {}".format(data_dict["min_size"],
        data_dict["max_size"]), fontsize=10)
    plotlib.xlabel('Number of threads')
    # bench-malloc-thread uses RDTSC counter for reporting time => CPU clock cycles
    plotlib.ylabel('CPU cycles per sum of (1 free + 1 malloc) op')

    nmarker=0
    max_x=[]
    max_y=[]
    for impl_name in benchmark_dict.keys():
        data_list_of_dicts = benchmark_dict[impl_name]
        # print("data_list_of_dicts = {}".format(data_list_of_dicts))

        # add a line plot
        X = [x["threads"] for x in data_list_of_dicts]
        Y = [y["time_per_iteration"] for y in data_list_of_dicts]

        lines = plotlib.plot(X, Y, '-' + filled_markers[nmarker], label=impl_name)
        plotlib.setp(lines, 'color', colours[nmarker])
        
        # remember max X/Y
        # In case you only ran some of the tests, don't attempt to get `max()` on an empty list--ie:
        # for a benchmark you didn't run. Only operate if the lists aren't empty.
        if X:
            max_x.append(max(X))
        if Y:
            max_y.append(max(Y))
        
        nmarker=nmarker+1

    # set some graph global props:        
    plotlib.xlim(0, max(max_x)*1.1)
    plotlib.ylim(0, max(max_y)*1.3)

    outfilename_dir = os.path.dirname(outfilename)
    print("Writing plot into '%s'" % outfilename)
    print(("- - -\n" +
          "Close the plot to terminate the program. Run `RESULT_DIRNAME='{}' make plot_results`\n" +
          "to plot the results again.\n" +
          "- - -").format(outfilename_dir))
    plotlib.legend(loc='upper left')
    plotlib.savefig(outfilename)
    plotlib.show()


def main(args):
    """Program Entry Point
    """
    if len(args) < 2:
        print('Usage: %s <image-output-file> <file1> <file2> ...' % sys.argv[0])
        sys.exit(os.EX_USAGE)

    benchmark_dict = {}
    for filepath in args[1:]:
        print("Parsing '{}'...".format(filepath))
        with open(filepath, 'r') as benchfile:
            filename = os.path.basename(filepath)
            
            try:
                bench_list_of_dicts = json.load(benchfile)
            except Exception as ex:
                print("Invalid JSON file {}: {}".format(filepath, ex))
                sys.exit(2)
            # print(json.dumps(bench_list_of_dicts, sort_keys=True, indent=4,
            #     separators=(',', ': ')))

            benchmark_dict[filename] = []
            for bench in bench_list_of_dicts:
                data_dict = bench["functions"]["malloc"][""]
                benchmark_dict[filename].append(data_dict)
            
            print('  Found {} data points in {}...'.format(len(benchmark_dict[filename]), filepath))
            
    plot_graphs(args[0], benchmark_dict)

if __name__ == '__main__':
    main(sys.argv[1:])


