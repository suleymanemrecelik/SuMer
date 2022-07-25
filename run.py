import yacc
import sys

f=open(sys.argv[1] ,"r")
parseTree = yacc.compileCode(f)
if(parseTree is not None):
    parse = parseTree[0]
    parseWithLines = parseTree[1]
    defStartsFinishes = parseTree[2]
    totalLine = parseTree[3]
    lineCodes = parseTree[4]
    variableValues = dict()
    functions = dict()
    programCounter = 1
    elseDecider = False

def runCode(node):
    global programCounter
    global elseDecider
    if node[0] == "STRING" and isinstance(node[1] , str):

        return node[1][1:-1]
    
    if node[0] == "boolean" and isinstance(node[1] , bool):

        return node[1]
    
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
        variableValues[node[2]] = 0
        try:
            return runCode(node[3])
        except:
            return
    
    if node[0] == 'assign':
        if(node[1] in variableValues):
            variableValues[node[1]] = runCode(node[2])
            return node[1]
        else:
            print("\n" + "Error on Line: " + str(programCounter) + " : " + str(lineCodes[programCounter]) +
                  " - First declare the variable: "+ node[1])
            sys.exit()
            
    if node[0] == 'print':
        print(runCode(node[1]))
        return
    
    if node[0] == '+':
        try:
            return runCode(node[1]) + runCode(node[2])
        except:
            return str(runCode(node[1])) + str(runCode(node[2]))
    if node[0] == '-':
        try:
            return runCode(node[1]) - runCode(node[2])
        except:
            return str(runCode(node[1])) - str(runCode(node[2]))
    if node[0] == '*':
        try:
            return runCode(node[1]) * runCode(node[2])
        except:
            print( "Error on Line: " + str(programCounter) + " : " + str(lineCodes[programCounter]) +
                  " - cannot multiply " + str(type(runCode(node[1]))) + " to " + str(type(runCode(node[2]))))
            sys.exit()
    if node[0] == '/':
        try:
            return runCode(node[1]) / runCode(node[2])
        except:
            print( "Error on Line: " + str(programCounter) + " : " + str(lineCodes[programCounter]) +
                  " - cannot divide " + str(type(runCode(node[1]))) + " to " + str(type(runCode(node[2]))))
            sys.exit()            

    if node[0] == '+=':
        variableValues[node[1][1]] = runCode(node[1]) + runCode(node[2])
        return variableValues[node[1][1]]
   
    if node[0] == '-=':
        variableValues[node[1][1]] = runCode(node[1]) - runCode(node[2])
        return node[1]
    
    if node[0] == '*=':
        variableValues[node[1][1]] = runCode(node[1]) * runCode(node[2])
        return node[1]
    
    if node[0] == '/=':
        variableValues[node[1][1]] = runCode(node[1]) / runCode(node[2])
        return node[1]
    
    if node[0] == 'VAR':
        try:
            return variableValues[node[1]]
        except LookupError:
            print("\n" + "Error on Line: " + str(programCounter) + " : " + str(lineCodes[programCounter]) +
                  " - First declare the variable: "+ node[1])
            sys.exit()
            return 0
        
    if node[0] == "&":
        return (runCode(node[1]) and runCode(node[2]))
    if node[0] == "|":
        return (runCode(node[1]) or runCode(node[2]))
    if node[0] == "<":
        return (runCode(node[1]) < runCode(node[2]))
    if node[0] == ">":
        return (runCode(node[1]) > runCode(node[2]))
    if node[0] == "?=":
        return (runCode(node[1]) == runCode(node[2]))
    if node[0] == "!<":
        return not((runCode(node[1]) < runCode(node[2])))
    if node[0] == "!>":
        return not((runCode(node[1]) > runCode(node[2])))
    if node[0] == "!?=":
        return not((runCode(node[1]) == runCode(node[2])))
    """if node[0] == "IF":
        return runCode(node[1])"""
    if(node[0]=="IF"):
        startLoc = programCounter+1
        finishLoc = defStartsFinishes[programCounter]
        if(runCode(node[1])):
            elseDecider = False
            programCounter = startLoc
            while (programCounter <= finishLoc):                  
                if programCounter in parseWithLines: 
                    runCode(parseWithLines[programCounter])
                programCounter += 1
            programCounter=finishLoc
        else:
            programCounter = finishLoc
            elseDecider = True
        return    
           
    if(node[0]=="ELS"):
        startLoc = programCounter+1
        finishLoc = defStartsFinishes[programCounter]
        if(elseDecider):
            programCounter = startLoc
            while (programCounter <= finishLoc):                  
                if programCounter in parseWithLines: 
                    runCode(parseWithLines[programCounter])
                programCounter += 1
            programCounter= finishLoc
        else:
            programCounter = finishLoc
        return
    
    if node[0] == "FUNCTION":
        functions[node[1]] = (programCounter+1, defStartsFinishes[programCounter])
        programCounter = defStartsFinishes[programCounter]
        return
    
    if node[0] == "CALL":
        currLoc = programCounter
        programCounter = functions[node[1]][0]
        while(programCounter <= functions[node[1]][1]):          
            if programCounter in parseWithLines: 
                runCode(parseWithLines[programCounter])
            programCounter +=1
        programCounter = currLoc
        return
    
    if(node[0]=="WHILE"):
        
        startLoc = programCounter+1
        finishLoc = defStartsFinishes[programCounter]
        if(runCode(node[1])):
            while(runCode(node[1])):
                programCounter = startLoc
                while (programCounter <= finishLoc):                  
                    if programCounter in parseWithLines: 
                        runCode(parseWithLines[programCounter])
                    programCounter += 1
            programCounter = finishLoc
            return
        else:
            programCounter = finishLoc
            return
        return
        
    if(node[0] == "FOR"):
        startLoc = programCounter+1
        finishLoc = defStartsFinishes[programCounter]
        runCode(node[1])
        if(runCode(node[2])):
            while(runCode(node[2])): 
               # for i in range (startLoc, finishLoc):
                programCounter = startLoc
                while (programCounter <= finishLoc):
                    if programCounter in parseWithLines: 
                        runCode(parseWithLines[programCounter])
                    programCounter += 1
                
                runCode(node[3])
            programCounter = finishLoc
            return  
        else:
            programCounter = finishLoc
            return

if(parseTree is not None):
    print("\nParse Tree: ")
    print(parse)
    print("\nProgram Output: ")
    
    while (programCounter <= totalLine):
        if programCounter in parseWithLines:
            tree = parseWithLines[programCounter]            
            runCode(tree)
            programCounter +=1

        else:
            programCounter +=1
            

        



    

