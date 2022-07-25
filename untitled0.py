from projectLexer import LexerClass
from projectParser import ParserClass
    
class Execution:
    
    def __init__(self, tree, env):
        self.env = env
        result = self.executionTree(tree)
        if result != None and isinstance(result, int):
            print(result)
        
        if isinstance(result, str) and result[0] == '"':
            print(result)   
    
    def executionTree(self, node):
        
        if isinstance(node , int):
            return node
                   
        if isinstance(node, str):
            return node
        
        if node is None:
            return None
        
        if node[0] == 'int':
            return node[1]

        if node[0] == 'condition_eq':
            return self.executionTree(node[1]) == self.executionTree(node[2])

        if node[0] == 'condition_lt':
            return self.executionTree(node[1]) < self.executionTree(node[2])
        
        if node[0] == 'condition_gt':
            return self.executionTree(node[1]) > self.executionTree(node[2])

        if node[0] == 'condition_le':
            return self.executionTree(node[1]) <= self.executionTree(node[2])
        
        if node[0] == 'condition_ge':
            return self.executionTree(node[1]) >= self.executionTree(node[2])

        if node[0] == 'condition_ne':
            return self.executionTree(node[1]) != self.executionTree(node[2])
        
        if node[0] == 'if_statement':
            result = self.executionTree(node[1])
            if result:
                return self.executionTree(node[2][1])
            return self.executionTree(node[2][2])
        
        if node[0] == 'str':
            return node[1]
       
        if node[0] == 'flt':
            return node[1]
        
        if node[0] == 'print':
            print(self.executionTree(node[1]))
        
        if node[0] == 'add':
            return self.executionTree(node[1]) + self.executionTree(node[2])
        if node[0] == 'sub':
            return self.executionTree(node[1]) - self.executionTree(node[2])
        if node[0] == 'mul':
            return self.executionTree(node[1]) * self.executionTree(node[2])
        if node[0] == 'div':
            return self.executionTree(node[1]) / self.executionTree(node[2])
        
        if node[0] == 'variable_assign':
            self.env[node[1]] = self.executionTree(node[2])
            return node[1]        

        if node[0] == 'var':
            try:
                return self.env[node[1]]
            except LookupError:
                print("ERROR! First define the variable "+node[1])
                return 0
    
        if node[0] == 'for_loop':
            if node[1][0] == 'for_loop_setup':
                loop = self.executionTree(node[1])
                decreasing_count = self.executionTree(node[1][3])
                count_for_loop = self.env[loop[0]]
                treshold = loop[1]
                
                for i in range(count_for_loop + decreasing_count , treshold + 1, decreasing_count):
                    result = self.executionTree(node[2])
                    if result != None:
                        print(result)
                    self.env[loop[0]] = i
                
        if node[0] == 'for_loop_setup':
            return (self.executionTree(node[1]), self.executionTree(node[2]))
        
        if node[0] == 'func_def':
            self.env[node[1]] = node[2]

        if node[0] == 'func_print':
            try:
                return self.executionTree(self.env[node[1]])
            except LookupError:
                print("Undefined function '%s'" % node[1])
                return 0
        
if __name__ == '__main__':
    lexer = LexerClass()
    parser = ParserClass()
    env = {}
    while True:
        try:
            text = input('write the code here-> ')
            if text == "break":
                break
        except EOFError:
            break
        if text:
            tree = parser.parse(lexer.tokenize(text))
            Execution(tree, env)
            