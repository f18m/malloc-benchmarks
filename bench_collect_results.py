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
jemalloc_install_dir = 'jemalloc-install'

impl_preload_libs = [
           '', 
           tcmalloc_install_dir + '/lib/libtcmalloc.so',
           jemalloc_install_dir + '/lib/libjemalloc.so'
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
    
    
def check_requirements():
    global required_libs_fullpaths
    
    if not os.path.isfile(benchmark_util):
        print("Could not find required benchmarking utility {}".format(benchmark_util))
        sys.exit(2)
    print("Found required benchmarking utility {}".format(benchmark_util))

    for preloadlib in impl_preload_libs:
        if len(preloadlib)>0:
            if not os.path.isfile(preloadlib):
                print("Could not find required lib {}".format(preloadlib))
                sys.exit(2)
            print("Found required lib {}".format(preloadlib))

    for reqlib in required_libs:
        full_path = find(reqlib, ['/usr/lib', '/lib'])
        if len(full_path)==0:
            print("Could not find required shared library {}".format(reqlib))
            sys.exit(2)
        required_libs_fullpaths.append(full_path)

def run_benchmark(outfile,thread_values,impl_idx):
    global required_libs_fullpaths, impl_preload_libs
    
    of = open(outfile, 'w')
    of.write('[')
    
    success = 0
    last_nthreads = thread_values[len(thread_values)-1]
    bm = {}
    for nthreads in thread_values:

        try:
            os.environ["LD_PRELOAD"] = impl_preload_libs[impl_idx]
            if len(os.environ["LD_PRELOAD"])>0:
                # the tcmalloc/jemalloc shared libs require in turn C++ libs:
                #print "required_libs_fullpaths is:", required_libs_fullpaths
                for lib in required_libs_fullpaths:
                    os.environ["LD_PRELOAD"] = os.environ["LD_PRELOAD"] + ':' + lib
                    
            # run the external benchmark utility with the LD_PRELOAD trick
            print("Running benchmark for nthreads={} with LD_PRELOAD='{}'".format(nthreads,os.environ["LD_PRELOAD"]))
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

def main(args):
    """Program Entry Point
    """
    if len(args) < 2:
        print('Usage: %s <output filename postfix> <num threads test1> <num threads test2> ...' % sys.argv[0])
        sys.exit(os.EX_USAGE)

    outfile_postfix = args[0]
    success = 0
    
    check_requirements()
    
    for idx in range(0,len(implementations)):
        outfile = implementations[idx] + '-' + outfile_postfix
        print "Testing implementation '{}'. Saving results into '{}'".format(implementations[idx],outfile)
        
        thread_values = args[1:]
        print "Will run tests for {} different number of threads".format(len(thread_values))
    
        success = success + run_benchmark(outfile,thread_values,idx)

    return success

if __name__ == '__main__':
    success = main(sys.argv[1:])
    if success==0:
        sys.exit(1)
        
