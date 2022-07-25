import ply.yacc as yacc
import re
 # Get the token map from the lexer.  This is required.
from lex import tokens 
import sys

def p_statements_multiple(p):
    '''
    statements : statements statement

    '''
    p[0] = p[1] + [ p[2] ]
def p_statements_single(p):
    '''
    statements : statement

    '''
    p[0] = [p[1]]
    
def p_statement_parameter(p):
    '''
    statement : statement COMMA statement
    '''
    p[0] = [p[1], p[3]]   
def p_statement_FUNCTION(p):
    '''
    statement : FUNCTION VAR LPAREN statement RPAREN DEFSTART
    '''
    p[0] = ('FUNCTION', p[2], p[4], p[6])

def p_statement_FUNCTION_empty(p):
    '''
    statement : FUNCTION VAR LPAREN RPAREN DEFSTART
    '''
    p[0] = ('FUNCTION', p[2], p[5])
    
def p_statement_call_FUNCTION(p):
    '''
    statement : CALL VAR LPAREN statement RPAREN
    '''
    p[0] = ('CALL', p[2], p[4])
    
def p_statement_call_FUNCTION_empty(p):
    '''
    statement : CALL VAR LPAREN RPAREN
    '''
    p[0] = ('CALL', p[2])
    
def p_loop_statement_WHILE(p):
    '''
    statement : WHILE LPAREN expr RPAREN DEFSTART
    '''
    p[0] = ('WHILE', p[3], p[5])

def p_loop_statement_FOR(p):
    '''
    statement : FOR LPAREN statement SEMICOLON expr SEMICOLON statement RPAREN DEFSTART
    '''
    p[0] = ('FOR', p[3], p[5], p[7], p[9])

def p_condition_statement(p):
    '''
    statement : IF LPAREN expr RPAREN DEFSTART
            | ELSEIF LPAREN expr RPAREN DEFSTART
    '''
    
    p[0] = (p[1].upper(), p[3], p[5] )
def p_condition_statement_ELSE(p):
    '''
    statement : ELSE DEFSTART
            
    '''
    
    p[0] = (p[1].upper(), p[2] )
    
def p_declaration_statement(p):
    '''
    statement : DVAR VAR
    '''
    p[0] = ('declare', p[1], p[2])

def p_initialization_statement(p):
    '''
    statement : VAR EQUAL expr
    '''
    p[0] = ('assign', p[1], p[3])
    
    
def p_dec_init_statement(p):
    '''
    statement : DVAR VAR EQUAL expr           
    '''
    p[0] = ('declare', p[1], p[2], ('assign', p[2], p[4]))
    
def p_declaration_statement_ARRAY(p):
    '''
    statement : ARRAY VAR
    '''
    p[0] = ('declare', p[1], p[2])

def p_initialization_statement_ARRAY(p):
    '''
    statement : VAR EQUAL LCB expr RCB 
    '''
    p[0] = ('assign', p[1], p[4])
    
def p_dec_init_statement_ARRAY(p):
    '''
    statement : ARRAY VAR EQUAL LCB expr RCB
             
    '''
    p[0] = ('declare', p[1], p[2], ('assign', p[2], p[5]))
    
    
def p_initialization_ARR_expr(p):
    '''
    expr : expr COMMA expr
    '''
    p[0] = [p[1]]
    p[0] += p[3]

def p_print_statement(p):
    '''
    statement : PRINT LPAREN expr RPAREN
    
    '''
    p[0] = ('print', p[3])

def p_expr_binop(p):
    '''
    expr : expr PLUS expr 
        | expr MINUS expr
        | expr TIMES expr
        | expr DIVIDE expr
        | expr AND expr
        | expr OR expr
    '''
    p[0] = (p[2], p[1], p[3])
    
def p_statement_fbinop(p):
    '''
    statement : expr FPLUS expr 
            | expr FMINUS expr
            | expr FTIMES expr
            | expr FDIVIDE expr
    '''
    p[0] = (p[2], p[1], p[3])
    
def p_expr_conditions(p):
    '''
    expr : expr ISEQUAL expr 
        | expr SMALLER expr
        | expr GREATER expr
    '''
 
    p[0] = (p[2], p[1], p[3])

        
def p_expr_conditions_NOT(p):
    '''
    expr : expr NOT ISEQUAL expr
         | expr NOT SMALLER expr
         | expr NOT GREATER expr
    '''
    p[0] = (p[2]+p[3], p[1], p[4])
    
def p_expr_NUM(p):
    '''
    expr : NUMBER
    '''
    p[0] = ('number',p[1])
    
def p_expr_DNUM(p):
    '''
    expr : DNUMBER
    '''
    p[0] = ('dnumber',p[1])
    
def p_expr_BOOLEAN(p):
    '''
    expr : BOOLEAN
    '''
    p[0] = ('boolean',p[1])
    
def p_expr_VAR(p):
    '''
    expr : VAR
    ''' 
    p[0] = ('VAR', p[1])
    
def p_expr_STRING(p):
    '''
    expr : STRING
    ''' 
    p[0] = ('STRING', p[1])
    
def p_expr_group(p):
    '''
    expr : LPAREN expr RPAREN
    '''
    p[0] = p[2]
    
def p_expr_DEFFINISH(p):
    '''
    statement : DEFFINISH
    '''
    p[0] = ('DEFFINISH', p[1])
# Error rule for syntax errors
def p_error(p):
    print("Syntax error in input!")

# Build the parser
parser = yacc.yacc()

#f=open("codee.txt" ,"r")

#print(dataa)
#print(parser.parse(data))
lines = dict()
linesCodes = dict()
defStartsFinishes = dict()
defStack = []
def compileCode(f):
    data = f.read()
    data = re.sub(re.compile("\#.*?\#",re.DOTALL ) ,"" ,data)
    dataSplit = data.split("\n")
    lineCounter = 1
    success = True
    errors = dict()
    lineCodes = dict()
    for s in dataSplit:
        if s.rstrip():
            parse = parser.parse(s)
            if(parse == None):
                success = False
                #print("ERROR: " + str(lineCounter) + "\t" + s + "\t")
                errors[lineCounter] = (s)
            else:
                
                #print(str(lineCounter) + "\t" + s + "\t" + str(parse))
                lines[lineCounter] = parse[0]
                lineCodes[lineCounter] = s
                if(success):
                    try: 
                        if(str(s).rstrip().endswith("->")):
                            defStack.append(lineCounter)
                        if(str(s).rstrip().endswith("<-")):
                            defStartsFinishes[defStack[-1]] = lineCounter
                            defStack.pop()
                    except:
                        print ("\nUnbalanced definition ( \"->\" and \"<-\") symbols")
                        success = False
               
        lineCounter += 1
    if(success):
        parseTree = parser.parse(data)
        print ("\nSuccessfully compiled, no syntax error")
        return parseTree, lines, defStartsFinishes, lineCounter, lineCodes
    else:
        print ("\nSyntax Error Found")
        for e in errors:
            print ("Invalid Syntax on Line: " + str(e) + ", " + str(errors[e]))
        return None

#compileCode(f)
    
    
    
    
    
    
    
    
    
    
    