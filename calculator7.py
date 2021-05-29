import re
from collections import deque

def check_format(expression):
    for token in expression:
        if token in ("+", "-", "=", "*", "/", "(", ")"):
            continue
        if token[0] in ("+", "-"):
            if token[1:].isnumeric():
                continue
        if token[-1] in ("+", "-"):
            if token[:len(token) - 1].isnumric():
                return False
        if token.isnumeric() or token.isalnum():
            continue
        return False
 
    return True

def get_expression(line):
    if line.find("**") != -1:
        return False, line
    if line.find("//") != -1:
        return False, line
    line = re.sub("--", "+", line)
    line = re.sub("\++", "+", line)
    line = re.sub("\+-", "-", line)
    line = re.sub("([=\*/\+\-\(\)])", " \\1 ", line)
    expression = line.split()
    result = check_format(expression)          
    return result, expression

def is_mynumeric(token):
    if token.isnumeric():
        return True
    if token[0] in ("+", "-"):
       if token[1:].isnumeric():
           return True
    return False
    
def svcalc(expression, variables):
    total = 0
    ope = "+"
    for i in range(len(expression)):
        token = expression[i]
        if i % 2 == 1:   
            ope = token
            continue
        if token.isalpha():
            if token in variables:
                token = variables[token]
            else:
                print("Unknown variable")
                return
        else:
            if not is_mynumeric(token):
                if i == 0 and len(expression) == 1:
                    print("Invalid identifier")
                else:
                    print("Invalid expression")
                return
        number = int(token)
        if ope == "+":
            total += number
        elif ope == "-":
            total -= number
    print(total)

def let(expression, variables):
    left = expression[0]
    if not left.isalpha():
        print("Invalid identifier")
        return
    if expression.count("=") > 1:
        print("Invalid assignment")
        return    
    if len(expression) != 3:
        print("Invalid expression")
        return
    left, ope, right = expression
    if ope != "=":
        print("Invalid expression")
        return
    if right.isalpha():
        if not right in variables:
            print("Unknown variable")
            return
        right = variables[right]
    else:
        if not is_mynumeric(right):
            print("Invalid assignment")
            return    

    variables[left] = right

def build_rpn(expression, variables):
# Add operands (numbers and variables) to the result (postfix notation) as they arrive.
# If the stack is empty or contains a left parenthesis on top, push the incoming operator on the stack.
# If the incoming operator has higher precedence than the top of the stack, push it on the stack.
# If the precedence of the incoming operator is lower than or equal to that of the top of the stack, pop the stack and add operators to the result until you see an operator that has smaller precedence or a left parenthesis on the top of the stack; then add the incoming operator to the stack.
# If the incoming element is a left parenthesis, push it on the stack.
# If the incoming element is a right parenthesis, pop the stack and add operators to the result until you see a left parenthesis. Discard the pair of parentheses.
# At the end of the expression, pop the stack and add all operators to the result.
    stack = deque()
    result = deque()
    for talken in expression:
        if talken in ("+", "-", "*", "/", "(", ")"):
            if len(stack) == 0:
                stack.append(talken)
            elif talken == "(":
                stack.append(talken)
            elif talken == ")":
                while len(stack) > 0 and stack[-1] != "(":
                    result.append(stack.pop()) 
                if len(stack) == 0:
                    return deque()
                else:
                    stack.pop()
            elif talken in ("*", "/"):
                if stack[-1] in ("+", "-"):
                    stack.append(talken)
                else:
                    while len(stack) > 0 and stack[-1] not in ("+", "-", "("):
                        result.append(stack.pop())
                    stack.append(talken)
            elif talken in ("+", "-"):
                    while len(stack) > 0 and stack[-1] != "(":
                        result.append(stack.pop())
                    stack.append(talken)    
        else:
            result.append(talken)
    for _i in range(len(stack)):
        result.append(stack.pop())

    if "(" in result:
        return deque()

    return result

def calc(rpn, variables):
# If the incoming element is a number, push it into the stack (the whole number, not a single digit!).
# If the incoming element is the name of a variable, push its value into the stack.
# If the incoming element is an operator, then pop twice to get two numbers and perform the operation; push the result on the stack.
# When the expression ends, the number on the top of the stack is a final result.    
    stack = deque()
    for talken in rpn:
        if talken in ("+", "-", "*", "/"):
            operand2 = stack.pop()
            operand1 = stack.pop() 
            if talken == "*":
                stack.append(operand1 * operand2)
            elif talken == "/":
                stack.append(operand1 / operand2)
            elif talken == "+":
                stack.append(operand1 + operand2)
            elif talken == "-":
                stack.append(operand1 - operand2)
        elif is_mynumeric(talken):
            stack.append(int(talken))
        else:
            if talken not in variables:
                print("Unknown variable")
                return
            talken = variables[talken]
            stack.append(int(talken))

    print(int(stack[-1]))

variables = {}
while True:
    line = input()
    if line == "":
        continue
    if line[0] == "/":
        if line == "/help":
            print("The program calculates plus, minus, multiply and divide and support variables")
            continue
        if line == "/exit":
            break
        print("Unknown command")
        continue
    result, expression = get_expression(line)
    if result == False:
        print("Invalid expression")
        continue
    if "=" in expression:
        let(expression, variables)
    else:
        rpn = build_rpn(expression, variables) 
        if len(rpn) == 0:
            print("Invalid expression")
            continue
        calc(rpn, variables) 

print("Bye!")