import yacc
import sys
    
class Execution:
      
    def __init__(self, tree, vv, line):
        self.vv = vv
        self.line = line
        result = self.executionTree(tree)
        if result != None and isinstance(result, int):
            print(result)
        
        if isinstance(result, str) and result[0] == '"':
            print(result)   
    
            
    def executionTree(self, node):
        if node[0] == "STRING" and isinstance(node[1] , str):

            return node[1][1:-1]
        
        if node[0] == "number" and isinstance(node[1] , int):
            return node[1]
        
        if node[0] == "dnumber" and isinstance(node[1] , float):
            return node[1]
        
        if isinstance(node, list):
            l = []
            for i in range(0, len(node)-2):
                l.append(node[i][1])
            l.append(node[-1])
            return l
        
        if node is None:
            return None
        
        if node[0] == 'declare':
            self.vv[node[2]] = 0
            try:
                return self.executionTree(node[3])
            except:
                return
        
        if node[0] == 'assign':
            if(node[1] in self.vv):
                self.vv[node[1]] = self.executionTree(node[2])
                return node[1]
            else:
                print("\n" + "Line: " + str(self.line) + " ERROR! First declare the variable: "+ node[1])
                sys.exit()
                
        if node[0] == 'print':
            print(self.executionTree(node[1]))
        
        if node[0] == '+':
            return self.executionTree(node[1]) + self.executionTree(node[2])
        if node[0] == '-':
            return self.executionTree(node[1]) - self.executionTree(node[2])
        if node[0] == '*':
            return self.executionTree(node[1]) * self.executionTree(node[2])
        if node[0] == '/':
            return self.executionTree(node[1]) / self.executionTree(node[2])              

        if node[0] == 'VAR':
            try:
                return self.vv[node[1]]
            except LookupError:
                print("\n" + "Line: " + str(self.line) + " ERROR! First declare the variable: "+ node[1])
                sys.exit()
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
    f=open("codee.txt" ,"r")
    parseTree = yacc.compileCode(f)
    parse = parseTree[0]
    parseWithLines = parseTree[1]
    variableValues = dict()
    if(parseWithLines != None):
    
        print(parse)
        for p in parseWithLines:
            tree = parseWithLines[p]
            Execution(tree, variableValues, p)

