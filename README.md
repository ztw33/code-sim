# code-sim
A tool for measuring the similarity between two c++ code files.

## Platform
Linux (Best: Ubuntu 18.04 LTS Bionic)

## Requirements
- python >= 3.6.9
- pip >= 18.0
- clang == 6.0.0
- libclang-dev == 6.0.0
- llvm == 6.0.0

Before installing codesim, make sure you have already installed python and pip. And install clang and llvm using command below:
```shell
$ sudo apt-get install clang-6.0 libclang-6.0-dev llvm-6.0
```
Make sure you can find the file "libclang.so" in the path which can been seen after you successfully execute "llvm-config --libdir".
```shell
$ llvm-config --libdir
/usr/lib/llvm-6.0/lib
```
## Installing
First you should clone this project:
```shell
$ git clone https://github.com/ztw33/code-sim.git
```
Enter the directory and install:
```shell
$ cd code-sim
$ pip install .
```
Now you can use command 'codesim' to measure the similarity between two c++ code files.

## Usage
```
usage: codesim [-h] [-v] [--mml MML] code1 code2

measure the similarity between two c++ code files

positional arguments:
  code1          the filepath of c++ code file1
  code2          the filepath of c++ code file2

optional arguments:
  -h, --help     show this help message and exit
  -v, --verbose  print detail information while measuring similarity
  --mml MML      minimum match length in GST algorithm when matching token
                 sequence (default: 3)
```
## Example
```shell
$ codesim test1.cpp test2.cpp
90.43

$ codesim test1.cpp test2.cpp -v
Finding libclang.so ......
Found libclang.so path in:  /usr/lib/llvm-6.0/lib/libclang.so 

Similar snippets:
================ 1 ================
test1.cpp: line 10 -- line 26
test2.cpp: line 9 -- line 18
================ 2 ================
test1.cpp: line 6 -- line 10
test2.cpp: line 5 -- line 8
================ 3 ================
test1.cpp: line 29 -- line 35
test2.cpp: line 23 -- line 29

Similarity: 90.43%
```
