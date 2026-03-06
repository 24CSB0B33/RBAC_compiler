import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from lexer import Lexer
from parser import Parser

def test_parser():
    input_code = """
    ROLE Teller
    {
        PERMIT initiate_transfer,save_transfer
    }

    ROLE Approver
    {
        PERMIT approve_transfer
    }

    CONFLICT Teller,Approver

    ROLE Dev_Admin INHERITS Teller,Approver
    {
        PERMIT read_logs
    }
    """
    
    # Pre-processing to remove comments
    # The example_dsl.txt has -> comments.
    
    print("--- Testing Lexer ---")
    try:
        lexer = Lexer(input_code)
        tokens = lexer.tokenize()
        print("Tokens:", tokens)
    except Exception as e:
        print("Lexer Error:", e)
        return

    print("\n--- Testing Parser ---")
    try:
        parser = Parser(tokens)
        ast = parser.parse()
        print("AST:", ast)
    except Exception as e:
        print("Parser Error:", e)

if __name__ == "__main__":
    test_parser()
