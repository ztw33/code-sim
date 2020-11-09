import argparse
import subprocess
import sys
import os
from clang.cindex import Config
from codesim.ast.AST import AST
from codesim.token_seq_match.GST import GST
# from clang.cindex import CursorKind

verbose = False
MML = 3  # minimum match length in GST

def parse_arg():
    parser = argparse.ArgumentParser(description="measure the similarity between two c++ code files")
    parser.add_argument("code1", type=str, help="the filepath of c++ code file1")
    parser.add_argument("code2", type=str, help="the filepath of c++ code file2")
    parser.add_argument("-v", "--verbose", action="store_true", help="print detail information while measuring similarity")
    parser.add_argument("--mml", type=int, default=3, help="minimum match length in GST algorithm when matching token sequence (default: 3)")
    return parser.parse_args()

def config_libclang():
    if verbose:
        print("Finding libclang.so ......")
    res = subprocess.Popen("llvm-config --libdir", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, encoding="utf-8").communicate()
    if len(res[1]) > 0:
        print("Something wrong with your llvm-config command.", file=sys.stderr)
        print(res[1], file=sys.stderr)
        exit(1)    
    libclang_path = res[0].strip() + "/libclang.so"
    if verbose:
        print("Found libclang.so path in: ", libclang_path, "\n")
    Config.set_library_file(libclang_path)

def main():
    args = parse_arg()
    global verbose
    verbose = args.verbose
    global MML
    MML = args.mml
    if not (os.path.exists(args.code1) and os.path.exists(args.code2)):
        print("Cannot find the files! Please check the file path.", file=sys.stderr)
        exit(1)
    
    config_libclang()

    ast1 = AST(args.code1)
    ast1.parse()
    ast2 = AST(args.code2)
    ast2.parse()
    
    token_list1 = ast1.get_tokens()
    tokens1 = [token.kind.value for token in token_list1]
    token_list2 = ast2.get_tokens()
    tokens2 = [token.kind.value for token in token_list2]

    gst = GST(tokens1, tokens2, MML)
    gst.match()

    if verbose:
        tiles = gst.get_tiles()
        print("Similar snippets:")
        for i, tile in enumerate(tiles):
            print("================ %d ================" % (i + 1))
            start1 = tile[0] if tile[0] != 0 else tile[0] + 1
            start2 = tile[1] if tile[1] != 0 else tile[1] + 1
            print("%s: line %d -- line %d" % (args.code1, token_list1[start1].location.line, token_list1[tile[0]+tile[2]-1].location.line))
            print("%s: line %d -- line %d" % (args.code2, token_list2[start2].location.line, token_list2[tile[1]+tile[2]-1].location.line))
        print("\nSimilarity: %.2f%%" % (gst.similarity*100))
    else:
        print("%.2f" % (gst.similarity*100))

if __name__ == "__main__":
    main()
