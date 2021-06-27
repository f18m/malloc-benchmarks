# Benchmark utility sources

The sources collected here are a small subset of the GNU libc benchmarking utility for `malloc` implementations.

Please see `glibc/benchtests/bech-malloc-thread.c` for the most up-to-date source code.

You can obtain it here: https://www.gnu.org/software/libc/sources.html:
```bash
git clone https://sourceware.org/git/glibc.git
cd glibc
git checkout master
```

Mirror: https://github.com/bminor/glibc/tree/master/benchtests

See also: 
1. https://kazoo.ga/a-simple-tool-to-test-malloc-performance/


## Each of the above source files came from the following glibc paths:

```bash
glibc/benchtests/bench-malloc-simple.c # <=== this one
glibc/benchtests/bench-malloc-thread.c # <=== this one

glibc/benchtests/bench-timing.h # <=== this one

glibc$ find | grep hp-timing\.h
./sysdeps/powerpc/powerpc64/hp-timing.h
./sysdeps/powerpc/powerpc32/power4/hp-timing.h
./sysdeps/s390/hp-timing.h
./sysdeps/x86/hp-timing.h # <=== this one
./sysdeps/alpha/hp-timing.h
./sysdeps/sparc/sparc32/sparcv9/hp-timing.h
./sysdeps/sparc/sparc64/hp-timing.h
./sysdeps/ia64/hp-timing.h
./sysdeps/generic/hp-timing.h
./sysdeps/mach/hurd/hp-timing.h

glibc/sysdeps/generic/hp-timing-common.h # <=== this one

glibc$ find | grep _itoa\.h
./sysdeps/x86_64/x32/_itoa.h
./sysdeps/mips/mips64/n32/_itoa.h
./sysdeps/generic/_itoa.h # <=== this one

glibc/benchtests/json-lib.h # <=== this one
glibc/benchtests/json-lib.c # <=== this one
```
