import argparse
import subprocess
import sys
import os
from clang.cindex import Config
from clang.cindex import CursorKind
from clang.cindex import Index
from codesim.GST import GST_sim

exclude_types = set([(CursorKind.CALL_EXPR, "operator<<"),  # exclude I/O statement
                     (CursorKind.CALL_EXPR, "operator>>"),
                     (CursorKind.CALL_EXPR, "printf"),
                     (CursorKind.CALL_EXPR, "scanf"),
                     (CursorKind.USING_DIRECTIVE, "")])  # exclude "using namespace ..." statement

def get_tokens(cursor, filepath):
    def _traverse_preorder(cursor, token_list):  # There is a method called "walk_preorder" in Cursor class. Here we need to ignore some subtrees so we implement on our own.
        if cursor.location.file and cursor.location.file.name != filepath:
            return
        if (cursor.kind, cursor.spelling) in exclude_types:
            return
        
        token_list.append(cursor.kind.value)
        for child in cursor.get_children():
            _traverse_preorder(child, token_list)

    tokens = []
    _traverse_preorder(cursor, tokens)
    return tokens

def main():
    parser = argparse.ArgumentParser(description="measure the similarity between two c++ code files")
    parser.add_argument("code1", type=str, help="the filepath of c++ code file1")
    parser.add_argument("code2", type=str, help="the filepath of c++ code file2")
    parser.add_argument("-v", "--verbose", action="store_true", help="print detail information while measuring similarity")
    args = parser.parse_args()
    
    res = subprocess.Popen("llvm-config --libdir", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, encoding="utf-8").communicate()
    if len(res[1]) > 0:
        print("Something wrong with your llvm-config command.", file=sys.stderr)
        print(res[1], file=sys.stderr)
        exit(1)
    
    libclang_path = res[0].strip() + "/libclang.so"
    if args.verbose:
        print("libclang LD_LIBRARY_PATH: ", libclang_path, "\n")
    Config.set_library_file(libclang_path)

    if not (os.path.exists(args.code1) and os.path.exists(args.code2)):
        print("Cannot find the files! Please check the file path.", file=sys.stderr)
        exit(1)
    
    index = Index.create()
    token_list1 = get_tokens(index.parse(args.code1, args=["-std=c++11"]).cursor, args.code1)
    token_list2 = get_tokens(index.parse(args.code2, args=["-std=c++11"]).cursor, args.code2)

    if args.verbose:
        print("Token-list of code1:")
        for id in token_list1:
            print("\t", CursorKind.from_id(id).name)
        print("Token-list of code2:")
        for id in token_list2:
            print("\t", CursorKind.from_id(id).name)
        print("\n")

    print(GST_sim(token_list1, token_list2))

if __name__ == "__main__":
    main()
