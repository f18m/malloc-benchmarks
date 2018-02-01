#!/usr/bin/python
"""Generate benchmarking results in JSON form, using GNU libc benchmarking utility;
different allocators are injected into that utility by using LD_PRELOAD trick.
"""
import sys
import os
import pylab
import json
import subprocess

#
# Constants
#

implementations = [ 'glibc', 'tcmalloc', 'jemalloc' ]
benchmark_util = 'glibc-build/benchtests/bench-malloc-thread'
tcmalloc_install_dir = 'tcmalloc-install'
jemalloc_install_dir = 'tcmalloc-install'

preload = [
           '', 
           tcmalloc_install_dir + '/lib/libtcmalloc.so',
           jemalloc_install_dir + '/lib/libjemalloc.so:/usr/lib/x86_64-linux-gnu/libstdc++.so.6:/lib/x86_64-linux-gnu/libgcc_s.so.1' 
           ]

required_libs= [ 'libstdc++.so', 'libgcc_s.so.1' ]
required_libs_fullpaths = []

def find(name, paths):
    for path in paths:
        #print "Searching into: ", path
        for root, dirs, files in os.walk(path, followlinks=True):
            if name in files:
                return os.path.join(root, name)
    return ""
    
def main(args):
    """Program Entry Point
    """
    if len(args) < 2:
        print('Usage: %s <output filename postfix> <num threads test1> <num threads test2> ...' % sys.argv[0])
        sys.exit(os.EX_USAGE)

    outfile_postfix = args[0]
    success = 0
    
    if not os.path.isfile(benchmark_util):
        print("Could not find required benchmarking utility {}".format(benchmark_util))
        sys.exit(2)

    for reqlib in required_libs:
        full_path = find(reqlib, ['/usr/lib', '/lib'])
        if len(full_path)==0:
            print("Could not find required shared library {}".format(reqlib))
            sys.exit(2)
        required_libs_fullpaths.append(full_path)

    for idx in range(0,len(implementations)):
        outfile = implementations[idx] + '-' + outfile_postfix
        print "Testing implementation '{}'. Saving results into '{}'".format(implementations[idx],outfile)
        
        thread_values = args[1:]
        print "Will run tests for {} different number of threads".format(len(thread_values))
    
        of = open(outfile, 'w')
        of.write('[')
        
        last_nthreads = thread_values[len(thread_values)-1]
        bm = {}
        for nthreads in thread_values:
            print "Running benchmark for nthreads={}".format(nthreads)

            try:
                os.environ["LD_PRELOAD"] = preload[idx]
                if len(os.environ["LD_PRELOAD"])>0:
                    # the tcmalloc/jemalloc shared libs require in turn C++ libs:
                    for lib in required_libs_fullpaths:
                        os.environ["LD_PRELOAD"] = os.environ["LD_PRELOAD"] + ':' + lib
                        
                # run the external benchmark utility with the LD_PRELOAD trick
                stdout = subprocess.check_output([benchmark_util, nthreads])
                            
                # produce valid JSON output:
                of.write(stdout)
                if nthreads != last_nthreads:
                    of.write(',')
                success=success+1
                
            except OSError as ex:
                print("Failed running malloc benchmarking utility: {}. Skipping.".format(ex))
    
        of.write(']')

    return success

if __name__ == '__main__':
    success = main(sys.argv[1:])
    if success==0:
        sys.exit(1)
        
