STOP_WORD = 'STOP'
ERROR_NEWICK_END = 'Newick does not have ";"!'
ERROR_IMBALANCED_BRACKETS = 'Newick tree brackets are not balanced!'
ERROR_NAME = 'Invalid name format!'
ERROR_NUMBER = 'Invalid number format!'
ERROR_DUPLICATE_NODE = 'Newick contains duplicates!'
CORRECT = 'Correct newick tree'
END_SYMBOL = ';'
NODE_SEPARATOR = ','
NAME_SEPARATOR = ':'


def main():
    print('Please, enter newick tree or enter "STOP" to finish')
    while True:
        newick = input()
        if newick == STOP_WORD:
            break
        print(check_newick(newick.strip()))


def check_newick(newick):
    invalid_numbers = (';', ':', ' ', '(', ')')
    invalid_nodes = (';', ' ', '(')
    if newick[len(newick) - 1] != END_SYMBOL:
        return ERROR_NEWICK_END
    current_node = ''
    current_number = ''
    nodes = []
    code = 0
    brackets_count = 0
    for i in newick[:len(newick)-1]:
        if i == '(':
            if code == 1:
                return ERROR_NUMBER
            brackets_count += 1
            continue
        if i == ')':
            brackets_count -= 1
            if brackets_count < 0:
                return ERROR_IMBALANCED_BRACKETS
            if code < 2:
                if code == 0:
                    if len(current_node) > 0:
                        if nodes.__contains__(current_node):
                            return ERROR_DUPLICATE_NODE
                        nodes.append(current_node)
                        current_node = ''
                code = 0
                current_number = ''
                continue
        if code == 0:
            if invalid_nodes.__contains__(i) or i.isdigit():
                return ERROR_NAME
            if i == NAME_SEPARATOR or i == NODE_SEPARATOR:
                if i == NAME_SEPARATOR:
                    code = 1
                else:
                    code = 2
                if len(current_node) > 0:
                    if nodes.__contains__(current_node):
                        return ERROR_DUPLICATE_NODE
                    nodes.append(current_node)
                current_node = ''
                if code == 1:
                    continue
            if i.isdigit() and not invalid_nodes.__contains__(i):
                current_node += i
        elif code == 1:
            if invalid_numbers.__contains__(i):
                return ERROR_NUMBER
            if i == NODE_SEPARATOR:
                code = 2
                current_number = ''
            else:
                if i.isdigit() or i == '.':
                    if (i == '.' and current_number.__contains__('.')) or (i == '.' and len(current_number) == 0):
                        return ERROR_NUMBER
                    if i != '.' and len(current_number) == 1 and current_number[0] == '0':
                        return ERROR_NUMBER
                    current_number += i
                elif i.isalpha():
                    return ERROR_NUMBER
        else:
            if i == NODE_SEPARATOR or i == ' ':
                code = 2
            else:
                if i.isdigit() or invalid_nodes.__contains__(i):
                    return ERROR_NAME
                code = 0
                current_node += i
    if brackets_count == 0:
        return CORRECT
    else:
        return ERROR_IMBALANCED_BRACKETS


main()