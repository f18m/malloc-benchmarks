# malloc-benchmarks
Simple benchmarking scripts to run on any machine to compare different C/C++ malloc implementations.

## How to collect benchmark results

```
   ./bench_collect_results.py my-malloc-results.json 1 2 4 8 16
```

## How to plot benchmark results

```
   ./bench_plot_results.py test.png *my-malloc-results.json
```

