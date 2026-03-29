import sys
from lexer import Lexer
from parser import Parser
from analyser import Analyser


def main():
    if len(sys.argv) < 2:
        print("Usage:python main.py <policy_file.rbac>")
        return
    
    filepath = sys.argv[1]

    try:
        with open(filepath, 'r') as f:
            source_code = f.read()

        print(f"---Compiling {filepath}---")


        #Lexing
        lexer = Lexer(source_code)
        tokens = lexer.tokenize()
        print("[OK] Lexical Analysis complete")

        #Parsing
        parser = Parser(tokens)
        ast = parser.parse()
        print("[OK] Syntax Parsing Complete (AST Generated)")

        #Semantic Analysis (all error checks)
        analyser = Analyser(ast)
        errors = analyser.run()
        

        if errors:
            print("\n[FAIL] Compilation Failed with errors.")

            for e in errors:
                print(f" {e}")
            sys.exit(1)
        else:
            print("[OK] Compilation successful with no errors.")

        #optimizing
        from optimizer import Optimizer
        opt = Optimizer(ast)
        optimized_ast = opt.optimize()
        print("[OK] AST Optimized (Redundancies Removed).")


    except FileNotFoundError:
        print(f"[ERROR] File not found:{filepath}")
        sys.exit(1)
    except SyntaxError as e:
        print(f"[ERROR] Syntax: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"[ERROR] {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
