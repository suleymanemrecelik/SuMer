import ply.lex as lex
 
 # List of token names.   This is always required
tokens = (
   'NUMBER',
   'DNUMBER',
   'BOOLEAN',
   'PLUS',
   'MINUS',
   'TIMES',
   'DIVIDE',
   'LPAREN',
   'RPAREN',
   'KEYWORD',
   'EQUAL',
   'ISEQUAL',
   'DEFSTART',
   'DEFFINISH',
   'VAR',
   'STRING',
   'TRUE',
   'FALSE',
   'AND',
   'OR',
   'GREATER',
   'SMALLER',
   'SEMICOLON',
   'COMMA',
   'NOT',
   'FPLUS',
   'FMINUS',
   'FTIMES',
   'FDIVIDE',
   'LCB',
   'RCB',
   'LSP',
   'RSP',
   'NEWLINE',
   
)

keywords = {
    
    'if' : 'IF',
    'els' : 'ELSE',
    'whl' : 'WHILE',
    'eif' : 'ELSEIF',
    'for' : 'FOR',
    'arr' : 'ARRAY', 
    'prt' : 'PRINT',
    'fnc' : 'FUNCTION',
    'var' : 'DVAR',
    "cal" : 'CALL'

}
 
 # Regular expression rules for simple tokens
t_PLUS    = r'\+'
t_MINUS   = r'\-'
t_TIMES   = r'\*'
t_DIVIDE  = r'/'
t_RPAREN  = r'\)'
t_LPAREN  = r'\('
t_EQUAL   = r'\='
t_ISEQUAL = r'\?=' 
t_DEFSTART  = r'\->'
t_DEFFINISH  = r'\<-'
t_AND  = r'\&'
t_OR  = r'\|'
t_GREATER  = r'\>'
t_SMALLER  = r'\<'
t_SEMICOLON  = r'\;'
t_NOT  = r'\!'
t_FPLUS    = r'\+='
t_FMINUS   = r'\-='
t_FTIMES   = r'\*='
t_FDIVIDE  = r'/='
t_COMMA = r'\,'
t_LCB = r'\{'
t_RCB = r'\}'
t_LSP = r'\['
t_RSP = r'\]'
t_NEWLINE = r'\n+'

 # A regular expression rule with some action code
tokens = tokens + tuple(keywords.values())

def t_BOOLEAN(t):
    r"True|False"
    t.value = t.value == 'True'
    return t

def t_VAR(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    t.value = str(t.value)
    t.type = keywords.get(t.value,'VAR')    # Check for reserved words
    return t

def t_STRING(t):
    r'"([^"\n]|(\\"))*"'
    t.value = str(t.value)
    return t




def t_DNUMBER(t):
    '\d+\.\d+'
    '[-+]?[0-9]+(\.([0-9]+)?([eE][-+]?[0-9]+)?|[eE][-+]?[0-9]+)'        
    t.value = float(t.value)  
    return t

def t_NUMBER(t):
    r'\d+'
    t.value = int(t.value)    
    return t


"""def t_TRUE(t):
    r'TRUE'
    t.value = True
    return t

def t_FALSE(t):
    r'FALSE'
    t.value = False
    return t"""

    
# Define a rule so we can track line numbers
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

def t_comment_ignore(t): 
    r'\#([^"\n]|(\\"))*\#'
    pass
# A string containing ignored characters (spaces and tabs)
t_ignore = ' \t\r'

# Error handling rule
def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)

# Build the lexer
lexer = lex.lex()
# Test it out
data = '''
var a = 10
var b = 4

fnc myFunction() ->
prt("my function is called") <-

for(var i=0; i<4; i+=1) ->
prt("i= " + i) <-

whl (a > 0) ->
if (a < 5) ->
prt (a + " is smaller then 5") 
<-
els ->
	if( a ?= 5) ->
	prt (a + " is equal to 5") 
	<-
	els ->
	prt (a + " is greater then 5") 
	<- 
<-
a -= 1 
<-

cal myFunction()
'''
"""lexer.input(data)
for tok in lexer:
    print(tok)"""