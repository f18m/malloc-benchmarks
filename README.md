# malloc-benchmarks

Simple benchmarking scripts to run on any machine to compare different C/C++ malloc implementations.
The scripts are not meant to face any possible problem, quite the opposite.
They will:
 - download and build [GNU libc](https://www.gnu.org/software/libc/), [Google perftools](https://github.com/gperftools/gperftools), [Jemalloc](http://jemalloc.net/)
 - use GNU libc malloc multi-thread benchmarking utility to generate JSON results for different combinations
   of malloc implementation and number of threads
 - use Python matplotlib to produce a summary figure


## How to collect benchmark results and view them

```
   git clone https://github.com/f18m/malloc-benchmarks.git
   cd malloc-benchmarks
   make
```
