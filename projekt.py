import sys
from antlr4 import *
from CPPLexer import CPPLexer
from CPPParser import CPPParser


def convert_to_python(tree, parser, indent_level=0):

    if tree.getChildCount() == 0:
        return tree.getText()


    rule_name = parser.ruleNames[tree.getRuleIndex()]


    indent = "    " * indent_level



    if rule_name == "program":
        return "\n".join([convert_to_python(child, parser, indent_level) for child in tree.children])
    elif rule_name == "preprocessorDirective":

        return ""
    elif rule_name == "emptyStatement":

        return ""

    elif rule_name == "namespaceDirective":

        return ""
    elif rule_name =="arrayFun":
        mem = tree.getText()
        mem = mem[0:len(mem)-1]
        return mem



    elif rule_name == "arrayDeclaration":
        array_name = tree.getChild(1).getText()
        size = tree.getChild(3).getText()
        return f"{indent}{array_name} = [None] * {size}"
    elif rule_name == "arrayAssignment":
        array_name = tree.getChild(0).getText()
        index = tree.getChild(2).getText()
        value = convert_to_python(tree.getChild(5), parser, 0)
        return f"{indent}{array_name}[{index}] = {value}"



    elif rule_name == "variableDeclaration":

        var_name = tree.getChild(1).getText()
        value = convert_to_python(tree.getChild(3), parser, 0)
        return f"{indent}{var_name} = {value}"
    elif rule_name == "emptyVariableDeclaration":

        var_name = tree.getChild(1).getText()
        return f"{indent}{var_name}"

    elif rule_name == "variableChange":
        var_name = tree.getChild(0).getText()
        value = convert_to_python(tree.getChild(2), parser, 0)
        return f"{indent}{var_name} = {value}"

    elif rule_name == "functionDeclaration":
        func_name = tree.getChild(1).getText()
        params = convert_to_python(tree.getChild(3), parser, 0) if tree.getChild(3).getText() != ')' else ''
        if tree.getChild(3).getText() != ')':
            help = 5
        else:
            help = 4
        body = convert_to_python(tree.getChild(help), parser, indent_level + 1)

        return f"{indent}def {func_name}({params}):\n{body}"

    elif rule_name == "functionCall":
        func_name = tree.getChild(0).getText()
        args = convert_to_python(tree.getChild(2), parser, 0) if tree.getChildCount() > 2 else ''
        return f"{indent}{func_name}({args})"

    elif rule_name == "argumentList":
        return ", ".join([convert_to_python(child, parser, 0) for child in tree.children if child.getText() != ','])

    elif rule_name == "parameterList":
        return ", ".join([convert_to_python(child, parser, 0) for child in tree.children if child.getText() != ','])

    elif rule_name == "parameter":
        return tree.getChild(1).getText()

    elif rule_name == "forStatement":
        init = convert_to_python(tree.getChild(2), parser, indent_level)
        condition = convert_to_python(tree.getChild(3), parser, 0)
        increment = convert_to_python(tree.getChild(5), parser, indent_level + 1)
        body = convert_to_python(tree.getChild(7), parser, indent_level + 1)
        return f"{init}\n{indent}while {condition}:\n{body}\n{increment}"

    elif rule_name == "whileStatement":
        condition = convert_to_python(tree.getChild(2), parser, 0)
        body = convert_to_python(tree.getChild(4), parser, indent_level + 1)
        return f"{indent}while {condition}:\n{body}"

    elif rule_name == "doWhileStatement":
        body = convert_to_python(tree.getChild(1), parser, indent_level + 1)
        condition = convert_to_python(tree.getChild(4), parser, 0)
        return f"{indent}while True:\n{body}\n{indent}    if not ({condition}):\n{indent}        break"



    elif rule_name == "block":
        instructions = [
            convert_to_python(child, parser, indent_level) for child in tree.children[1:-1]
        ]
        return "\n".join(instructions)

    elif rule_name == "ifStatement":
        result = ""

        condition = convert_to_python(tree.getChild(2), parser, 0)
        if_body = convert_to_python(tree.getChild(4), parser, indent_level + 1)
        result += f"{indent}if {condition}:\n{if_body}"


        i = 5
        while i < tree.getChildCount():
            if tree.getChild(i).getText() == "else if":
                elif_condition = convert_to_python(tree.getChild(i + 2), parser, 0)
                elif_body = convert_to_python(tree.getChild(i + 4), parser, indent_level + 1)
                result += f"\n{indent}elif {elif_condition}:\n{elif_body}"
                i += 4
            elif tree.getChild(i).getText() == "else":

                else_body = convert_to_python(tree.getChild(i + 1), parser, indent_level + 1)
                result += f"\n{indent}else:\n{else_body}"
                break
            i += 1
        return result

    elif rule_name == "incrementExpression":
        var_name = tree.getChild(0).getText()
        operator = tree.getChild(1).getText()
        if operator == "++":
            return f"{indent}{var_name} += 1"
        elif operator == "--":
            return f"{indent}{var_name} -= 1"

    elif rule_name == "returnStatement":
        value = convert_to_python(tree.getChild(1), parser, 0)
        return f"{indent}return {value}"



    elif rule_name == "coutStatement":

        output = []

        for i in range(2, tree.getChildCount(), 2):

            if tree.getChild(i).getText() == "endl":

                output.append("'\\n'")

            else:

                output.append(convert_to_python(tree.getChild(i), parser, 0))

        return f"{indent}print({', '.join(output)})"



    elif rule_name == "cinStatement":



        inputs = []

        for i in range(2, tree.getChildCount(), 2):

            var_name = convert_to_python(tree.getChild(i), parser, 0)

            inputs.append(f"{indent}{var_name} = input()")

        return "\n".join(inputs)

    elif rule_name == "compareExpression":

        if tree.getChildCount() == 1:

            return tree.getChild(0).getText()

        elif tree.getChildCount() == 2:

            operator = tree.getChild(0).getText()

            expression = convert_to_python(tree.getChild(1), parser, 0)

            if operator == "!":
                operator = "not"

            return f"{operator} {expression}"

        elif tree.getChildCount() == 3:

            left = convert_to_python(tree.getChild(0), parser, 0)

            operator = tree.getChild(1).getText()

            right = convert_to_python(tree.getChild(2), parser, 0)



            if operator == "&&":

                operator = "and"

            elif operator == "||":

                operator = "or"

            return f"{left} {operator} {right}"


    elif rule_name == "arithmeticExpression":
        if tree.getChildCount() == 1:
            return tree.getChild(0).getText()
        elif tree.getChildCount() == 3:
            left = convert_to_python(tree.getChild(0), parser, 0)
            operator = tree.getChild(1).getText()
            right = convert_to_python(tree.getChild(2), parser, 0)
            return f"{left} {operator} {right}"
    if rule_name == "STRING":
        return tree.getText()



    return "\n".join([convert_to_python(child, parser, indent_level) for child in tree.children])

def main():


    file_name = "test.cpp"

    try:

        with open(file_name, "r") as file:
            input_code = file.read()
    except FileNotFoundError:
        print(f"Plik '{file_name}' nie został znaleziony.")
        sys.exit(1)


    input_stream = InputStream(input_code)
    lexer = CPPLexer(input_stream)
    token_stream = CommonTokenStream(lexer)
    parser = CPPParser(token_stream)
    tree = parser.program()


    python_code = convert_to_python(tree, parser)
    print("\nTranslated Python code:\n")
    print(python_code)

    print(tree.toStringTree(recog=parser))


if __name__ == "__main__":
    main()



