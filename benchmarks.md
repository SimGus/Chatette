# Benchmarks
The following benchmarks were made using the Haskell package [bench](http://hackage.haskell.org/package/bench) and executed using *Python 3.6.8* on the examples located at *examples/complex/metal-work*.
The different benchmarkings were made in the closest situations possible.

The results show here are the direct output of the following command (or equivalent for older versions):
```sh
python3 -m chatette examples/complex/metal-work/master.chatette -f
```

The results are then analyzed and discussed.

## Results
### v1.0.0
```
benchmarking python3 src/main.py examples/chatette-generator/gen-data-dls.chatette
time                 696.7 ms   (688.2 ms .. 707.5 ms)
                     1.000 R²   (NaN R² .. 1.000 R²)
mean                 676.1 ms   (666.5 ms .. 684.8 ms)
std dev              10.52 ms   (3.230 ms .. 13.03 ms)
variance introduced by outliers: 19% (moderately inflated)
```

### v1.1.0
```
benchmarking python3 src/main.py examples/chatette-generator/gen-data-dls.chatette
time                 861.0 ms   (838.3 ms .. 879.2 ms)
                     1.000 R²   (1.000 R² .. 1.000 R²)
mean                 832.5 ms   (818.0 ms .. 844.2 ms)
std dev              14.86 ms   (6.711 ms .. 19.72 ms)
variance introduced by outliers: 19% (moderately inflated)
```

### v1.1.1
```
benchmarking python3 src/main.py examples/chatette-generator/gen-data-dls.chatette
time                 863.9 ms   (846.9 ms .. 883.1 ms)
                     1.000 R²   (1.000 R² .. 1.000 R²)
mean                 834.3 ms   (818.2 ms .. 846.3 ms)
std dev              15.99 ms   (6.098 ms .. 21.64 ms)
variance introduced by outliers: 19% (moderately inflated)
```

### v1.1.2
```
benchmarking python3 src/main.py examples/chatette-generator/gen-data-dls.chatette
time                 815.7 ms   (784.7 ms .. 855.0 ms)
                     1.000 R²   (1.000 R² .. 1.000 R²)
mean                 796.3 ms   (789.9 ms .. 806.5 ms)
std dev              9.708 ms   (1.833 ms .. 12.73 ms)
variance introduced by outliers: 19% (moderately inflated)
```

### v1.1.3
```
benchmarking python3 src/main.py examples/chatette-generator/gen-data-dls.chatette
time                 818.5 ms   (801.6 ms .. 856.7 ms)
                     1.000 R²   (0.999 R² .. 1.000 R²)
mean                 790.6 ms   (777.1 ms .. 803.4 ms)
std dev              14.44 ms   (8.091 ms .. 20.20 ms)
variance introduced by outliers: 19% (moderately inflated)
```

### v1.1.4
```
benchmarking python3 src/main.py examples/chatette-generator/gen-data-dls.chatette
time                 800.8 ms   (764.2 ms .. 824.6 ms)
                     1.000 R²   (1.000 R² .. 1.000 R²)
mean                 769.4 ms   (756.5 ms .. 782.2 ms)
std dev              15.80 ms   (6.989 ms .. 19.83 ms)
variance introduced by outliers: 19% (moderately inflated)
```

### v1.1.5
```
benchmarking python3 -m chatette.run examples/complex/master.chatette
time                 826.1 ms   (814.1 ms .. 840.3 ms)
                     1.000 R²   (1.000 R² .. 1.000 R²)
mean                 798.4 ms   (779.7 ms .. 807.9 ms)
std dev              17.73 ms   (429.7 μs .. 21.88 ms)
variance introduced by outliers: 19% (moderately inflated)
```

### v1.2.0
```
benchmarking python3 -m chatette.run examples/complex/master.chatette
time                 840.9 ms   (789.6 ms .. 877.5 ms)
                     1.000 R²   (0.999 R² .. 1.000 R²)
mean                 812.4 ms   (797.6 ms .. 824.4 ms)
std dev              15.67 ms   (11.84 ms .. 18.63 ms)
variance introduced by outliers: 19% (moderately inflated)
```

### v1.2.1
```
benchmarking python3 -m chatette.run examples/complex/master.chatette
time                 824.2 ms   (804.8 ms .. 862.6 ms)
                     1.000 R²   (0.999 R² .. 1.000 R²)
mean                 795.6 ms   (781.0 ms .. 805.8 ms)
std dev              15.32 ms   (8.795 ms .. 21.56 ms)
variance introduced by outliers: 19% (moderately inflated)
```

### v1.2.2
```
benchmarking python3 -m chatette.run examples/complex/master.chatette
time                 815.6 ms   (793.3 ms .. 853.6 ms)
                     1.000 R²   (1.000 R² .. 1.000 R²)
mean                 798.3 ms   (792.9 ms .. 807.3 ms)
std dev              8.581 ms   (187.6 μs .. 10.51 ms)
variance introduced by outliers: 19% (moderately inflated)
```

### v1.2.3
```
benchmarking python3 -m chatette.run examples/complex/master.chatette
time                 805.6 ms   (751.0 ms .. 853.4 ms)
                     0.999 R²   (0.999 R² .. 1.000 R²)
mean                 780.8 ms   (768.9 ms .. 793.7 ms)
std dev              13.73 ms   (7.247 ms .. 19.33 ms)
variance introduced by outliers: 19% (moderately inflated)
```

### v1.3.0
```
benchmarking python3 -m chatette examples/complex/master.chatette
time                 932.5 ms   (886.8 ms .. 978.0 ms)
                     1.000 R²   (1.000 R² .. 1.000 R²)
mean                 906.8 ms   (897.3 ms .. 920.3 ms)
std dev              13.04 ms   (3.687 ms .. 17.67 ms)
variance introduced by outliers: 19% (moderately inflated)
```

### v1.3.1
```
benchmarking python3 -m chatette examples/complex/master.chatette
time                 1.018 s    (969.2 ms .. 1.091 s)
                     0.999 R²   (0.998 R² .. 1.000 R²)
mean                 985.2 ms   (969.9 ms .. 997.7 ms)
std dev              18.33 ms   (8.382 ms .. 25.62 ms)
variance introduced by outliers: 19% (moderately inflated)
```

### v1.3.2
```
benchmarking python3 -m chatette examples/complex/metal-work/master.chatette
time                 1.026 s    (979.0 ms .. 1.081 s)
                     1.000 R²   (0.999 R² .. 1.000 R²)
mean                 979.1 ms   (961.2 ms .. 997.0 ms)
std dev              23.40 ms   (8.952 ms .. 31.04 ms)
variance introduced by outliers: 19% (moderately inflated)
```

### v1.4.0
*Crashes*

### v1.4.1
*Crashes*

### v1.4.2
```
benchmarking python3 -m chatette examples/complex/metal-work/master.chatette
time                 1.148 s    (1.108 s .. NaN s)
                     0.999 R²   (0.998 R² .. 1.000 R²)
mean                 1.095 s    (1.074 s .. 1.121 s)
std dev              26.68 ms   (11.56 ms .. 36.86 ms)
variance introduced by outliers: 19% (moderately inflated)
```

### v1.5.0
```
benchmarking python3 -m chatette examples/complex/metal-work/master.chatette -f
time                 1.179 s    (1.131 s .. 1.212 s)
                     1.000 R²   (0.999 R² .. 1.000 R²)
mean                 1.136 s    (1.114 s .. 1.156 s)
std dev              23.07 ms   (18.12 ms .. 27.64 ms)
variance introduced by outliers: 19% (moderately inflated)
```

### v1.6.0
```
benchmarking python3 -m chatette examples/complex/metal-work/master.chatette -f
time                 3.867 s    (3.695 s .. 4.065 s)
                     1.000 R²   (0.999 R² .. 1.000 R²)
mean                 3.663 s    (3.566 s .. 3.746 s)
std dev              103.3 ms   (43.50 ms .. 139.3 ms)
variance introduced by outliers: 19% (moderately inflated)
```

### v1.6.1rc
```
benchmarking python3 -m chatette examples/complex/metal-work/master.chatette -f
time                 1.023 s    (978.3 ms .. 1.099 s)
                     0.999 R²   (0.999 R² .. 1.000 R²)
mean                 985.2 ms   (972.6 ms .. 1.005 s)
std dev              18.72 ms   (4.391 ms .. 23.89 ms)
variance introduced by outliers: 19% (moderately inflated)
```

## Analysis and discussion
Even though `bench` is a very well made tool, its results shouldn't be taken as
the "ground truth" but need to be discussed and put in perspective.
Those results clearly show a trend of the time of execution (both median and
average during several executions) going upwards with every minor release,
especially starting with v1.3.0.
This trend is something that was indeed noticed when using Chatette.

However, we can mitigate these results because of a few reasons:
- the template files used for those tests were always the same, which means
  they don't use the features introduced in latest releases to perform better
- `bench` "catches" writes to standard output and standard error, making
  programs that make a lot of console prints seem faster than they really are
- latest releases support some features (unused during these tests) that are
  still checked for at runtime, thus taking a little time to check
- those performance check don't account at all for
    + the quality and maintainability of the code
    + the ease-of-use and quality of the user experience
- later releases write output to several files, meaning they need to delete and
  create files again before writing the output, whereas older versions simply
  created a file or overwrote it if it existed, which is a task that is likely
  to take much fewer time
  
Something we can easily notice is the large increase in execution time that
happened for v1.6.0, which was due to a way too aggressice caching strategy.

