import lex,sys

keywords = ('Title','Chapter','Section')
Separators = ('dot','comma','semicolon','excl','qm','colon')

tokens = keywords + Separators + ('words','numbers','newline')

#regex
t_dot = r'\.'
t_comma = r','
t_semicolon = r';'
t_excl = r'!'
t_qm = r'\?'
t_colon = r':'
t_newline = r'\n'
t_numbers = r'([0-9]+\.[0-9]+)|([0-9]+)'
# t_words = r'[^ \r\n\t!\.,;?0-9]+')

words= r'[A-Za-z]+'
keydict={key:key for key in keywords}
# checking for reserved words
@lex.TOKEN(words)
def t_words(t):
	t.type=keydict.get(t.value,'words')
	return t



# A string containing ignored characters (spaces and tabs)
t_ignore  = ' \t'

# Error handling rule
def t_error(t):
	t.type="ERROR"
	t.lexer.skip(1)

# # Define a rule so we can track line numbers
# def t_newlines(t):
#      r'\n+'
#      t.lexer.lineno += len(t.value)


lexer=lex.lex() 

# file=open(sys.argv[1],'r')
# test=file.read()
# lex.input(test)

# # Tokenize
# while True:
#     tok = lex.token()
#     if not tok: 
#         break      # No more input
#     print(tok)