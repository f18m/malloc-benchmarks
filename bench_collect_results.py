#!/usr/bin/python
"""Generate benchmarking results in JSON form, using GNU libc benchmarking utility;
different allocators are injected into that utility by using LD_PRELOAD trick.
"""
import sys
import os
import pylab
import json
import subprocess

implementations = [ 'glibc', 'tcmalloc', 'jemalloc' ]
preload = ['', 
           '/usr/local/lib/libtcmalloc.so:/usr/lib/x86_64-linux-gnu/libstdc++.so.6:/lib/x86_64-linux-gnu/libgcc_s.so.1', 
           '/usr/local/lib/libjemalloc.so:/usr/lib/x86_64-linux-gnu/libstdc++.so.6:/lib/x86_64-linux-gnu/libgcc_s.so.1' ]
benchmark_util = 'glibc-build/benchtests/bench-malloc-thread'

def main(args):
    """Program Entry Point
    """
    if len(args) < 2:
        print('Usage: %s <output filename postfix> <num threads test1> <num threads test2> ...' % sys.argv[0])
        sys.exit(os.EX_USAGE)

    outfile_postfix = args[0]
    
    for idx in range(0,len(implementations)):
        outfile = implementations[idx] + '-' + outfile_postfix
        print "Testing implementation {}. Saving results into '{}'".format(implementations[idx],outfile)
        
        thread_values = args[1:]
        print "Will run tests for {} different number of threads".format(len(thread_values))
    
        of = open(outfile, 'w')
        of.write('[')
        
        last_nthreads = thread_values[len(thread_values)-1]
        bm = {}
        for nthreads in thread_values:
            print "Running benchmark for nthreads={}".format(nthreads)

            os.environ["LD_PRELOAD"] = preload[idx]
            stdout = subprocess.check_output([benchmark_util, nthreads])
            of.write(stdout)
            
            # produce valid JSON output:
            if nthreads != last_nthreads:
                of.write(',')
    
        of.write(']')

if __name__ == '__main__':
    main(sys.argv[1:])
