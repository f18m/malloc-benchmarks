# Glibc benchmark utility source code

The primary glibc malloc benchmarking utility is `glibc/benchtests/bech-malloc-thread.c`. It is automatically downloaded by this repo, then built and run when you call `make`.

You can manually obtain the glibc source code here: https://www.gnu.org/software/libc/sources.html:
```bash
git clone https://sourceware.org/git/glibc.git
cd glibc
git checkout master
```

Mirror: https://github.com/bminor/glibc/tree/master/benchtests

See also: 
1. https://kazoo.ga/a-simple-tool-to-test-malloc-performance/


## If you ever wish to manually build glibc and its benchtests, do so as follows:

References:
1. https://www.gnu.org/software/libc/manual/html_node/Configuring-and-compiling.html
1. This project's makefile
1. https://stackoverflow.com/questions/10412684/how-to-compile-my-own-glibc-c-standard-library-from-source-and-use-it/68153847#68153847


```bash
# IMPORTANT: begin AT THE SAME DIRECTORY LEVEL as the `glibc` source code 
# directory, NOT inside the `glibc` source code dir! In other words, if 
# you are in the correct dir, running `ls` will show the `glibc` source
# code dir (that you just cloned) inside the dir you are in.
mkdir -p glibc-build
mkdir -p glibc-install
cd glibc-build
../glibc/configure --prefix="$(realpath "../glibc-install")"
time make -j8  # build with 8 threads (jobs); on a fast laptop this takes ~3 min.
time make install # (optional: install to the `glibc-install` dir you created)

# Build the benchtests (everything inside the `glibc/benchtests` dir) too
time make bench-build -j8
# Now you have this file you can use for malloc speed tests, for instance!: 
#       ../glibc-build/benchtests/bench-malloc-thread

# To build **and run** all glibc benchtests, do:
time make bench
```

## If you'd like to manually extract the files you need to just build this benchtest, here are the paths of _some_ of them, to get you started:

**Note: this technique is Not recommended, since it's hard to track down all of the source files needed, and build settings. Instead, just build glibc and its bench tests from the entire glibc source code as shown above.**

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

glibc$ find | grep isa\.h
./sysdeps/x86_64/isa.h # <=== this one
./sysdeps/i386/i586/isa.h
./sysdeps/i386/i686/isa.h
./sysdeps/i386/isa.h
./sysdeps/x86/tst-ifunc-isa.h

glibc/include/libc-symbols.h # <=== this one
```
