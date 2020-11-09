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

Before installing codesim, make sure you have already installed python and pip. 
```shell
>$ sudo apt-get install clang-6.0 libclang-dev-6.0 llvm-6.0
```

## Usage
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

## Example
```shell
>$ codesim test/test1.cpp test/test2.cpp
90.43

>$ codesim test/test1.cpp test/test2.cpp
Finding libclang.so ......
Found libclang.so path in:  /usr/lib/llvm-6.0/lib/libclang.so 

Similar snippets:
================ 1 ================
testcase/1.cpp: line 10 -- line 26
testcase/2.format.cpp: line 9 -- line 18
================ 2 ================
testcase/1.cpp: line 6 -- line 10
testcase/2.format.cpp: line 5 -- line 8
================ 3 ================
testcase/1.cpp: line 29 -- line 35
testcase/2.format.cpp: line 23 -- line 29

Similarity: 90.43%
```