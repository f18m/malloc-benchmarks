#
# Downloads, configure and compiles 3 different software packages:
#  - GNU libc
#  - Google perftools (tcmalloc)
#  - jemalloc
#
# Tested with versions:
#  - GNU libc 2.26
#  - Google perftools (tcmalloc) 2.6.3
#  - jemalloc 5.0.1


#
# Constants
#

topdir=$(shell readlink -f .)

benchmark_result_json := $(shell hostname)-results.json
benchmark_result_png := $(shell hostname)-results.png

glibc_url := git://sourceware.org/git/glibc.git
tcmalloc_url := https://github.com/gperftools/gperftools.git
jemalloc_url := https://github.com/jemalloc/jemalloc.git

glibc_build_dir := $(topdir)/glibc-build
glibc_install_dir := $(topdir)/glibc-install
tcmalloc_install_dir := $(topdir)/tcmalloc-install
jemalloc_install_dir := $(topdir)/jemalloc-install
parallel_flags := -j4 


#
# Functions
#

#
# Targets
#

.PHONY: all download build collect_results

all: download build collect_results

download:
	@echo "Downloading all malloc implementations"
	@[ ! -d glibc ] && git clone $(glibc_url) || echo "glibc GIT repo seems to be already there"
	@[ ! -d gperftools ] && git clone $(tcmalloc_url) || echo "Google perftools GIT repo seems to be already there"
	@[ ! -d jemalloc ] && git clone $(jemalloc_url) || echo "Jemalloc GIT repo seems to be already there"

#
# A couple of notes about GNU libc:
#  1) building in source dir is not supported... that's why we build in separate folder
#  2) building only benchmark utilities is not supported... that's why we build everything
#
$(glibc_build_dir)/benchtests/bench-malloc-thread:
	@echo "Building GNU libc... go get a cup of coffee... this will take time!"
	mkdir -p $(glibc_build_dir)
	cd $(glibc_build_dir) && \
		../glibc/configure --prefix=$(glibc_install_dir) && \
		make $(parallel_flags) && \
		make $(parallel_flags) bench BENCHSET=malloc-thread
	[ -x $(glibc_build_dir)/benchtests/bench-malloc-thread ] && echo "GNU libc benchmarking utility is ready!" || echo "Cannot find GNU libc benchmarking utility! Cannot collect benchmark results"

$(tcmalloc_install_dir)/lib/libtcmalloc.so:
	cd gperftools && \
		./autogen.sh && \
		./configure --prefix=$(tcmalloc_install_dir) && \
		make && \
		make install

$(jemalloc_install_dir)/lib/libjemalloc.so:
	cd jemalloc && \
		./autogen.sh && \
		./configure --prefix=$(jemalloc_install_dir) && \
		make && \
		( make install || true )
		
build: $(glibc_build_dir)/benchtests/bench-malloc-thread \
		$(tcmalloc_install_dir)/lib/libtcmalloc.so \
		$(jemalloc_install_dir)/lib/libjemalloc.so
	@echo "Congrats! Successfully built all malloc implementations to test."
	
collect_results:
	@echo "Starting to collect performance benchmarks."
	./bench_collect_results.py $(benchmark_result_json) 1 2 4 8 16
	./bench_plot_results.py $(benchmark_result_png) *$(benchmark_result_json)

