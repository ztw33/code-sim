from clang.cindex import CursorKind
from clang.cindex import Index

exclude_types = set([(CursorKind.CALL_EXPR, "operator<<"),  # exclude I/O statement
                     (CursorKind.CALL_EXPR, "operator>>"),
                     (CursorKind.CALL_EXPR, "printf"),
                     (CursorKind.CALL_EXPR, "scanf"),
                     (CursorKind.USING_DIRECTIVE, "")])  # exclude "using namespace ..." statement

class AST(object):
    def __init__(self, filepath):
        self.filepath = filepath
    
    def parse(self):
        """
        Generate the AST and return root cursor.
        """
        index = Index.create()
        cursor = index.parse(self.filepath, args=["-std=c++11"]).cursor
        self.cursor = cursor

    def get_tokens(self):
        """
        Get token sequence from cursor when preordered traversing.(exclude node in 'exclude_types')
        """
        def _traverse_preorder(cursor, token_list):  # There is a method called "walk_preorder" in Cursor class. Here we need to ignore some subtrees so we implement on our own.
            if cursor.location.file and cursor.location.file.name != self.filepath:
                return
            if (cursor.kind, cursor.spelling) in exclude_types:
                return
            
            token_list.append(cursor)
            for child in cursor.get_children():
                _traverse_preorder(child, token_list)

        tokens = []
        _traverse_preorder(self.cursor, tokens)
        return tokens
