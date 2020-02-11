import yacc,sys
from lexer import lexer,tokens
import re

chapter_count=0

def add(a,b):
	res=[0,0,0,0]
	res[0]=a[0]+b[0]
	res[1]=a[1]+b[1]
	res[2]=a[2]+b[2]
	res[3]=a[3]+b[3]
	return res

def p_start(p):
	'start : thesis'

def p_newlines(p):
	'''newlines : newline newlines
				| newline '''

def p_paragraph(p):
	'paragraph : statements'
	p[0]= p[1]

def p_paragraphs(p):
	'''paragraphs : paragraph newlines paragraphs 
				  | paragraph newlines
				  | paragraph
	'''
	p[0]={'paracount':0,'statements':[0,0,0,0]}
	if len(p)!=4:
		p[0]['statements'] = p[1]
		p[0]['paracount']=1
	elif len(p)==4:
		p[0]['paracount']=1+p[3]['paracount']
		p[0]['statements'] = add(p[1],p[3]['statements'])


def p_statements(p):
	'''statements : statement statements 
				  | statement'''
	if len(p)==2:
		p[0]=p[1]
	else:
		p[0]=add(p[1],p[2])

def p_statement(p):
	'''statement : sentence excl 
				 | sentence dot
				 | sentence qm'''
	a,b,c=0,0,0
	if p[2]=='.':
		b=1
	elif p[2]=='!':
		a=1
	elif p[2]=='?':
		c=1
	d=p[1]
	p[0]=[a,b,c,d]

# def p_exclamation(p):
# 	'exclamation : sentence excl'

# def p_declaration(p):
# 	'declaration : sentence dot'

# def p_question(p):
# 	'question : sentence qm'

def p_sentence(p):
	'''sentence : sentenceword comma sentence
				| sentenceword semicolon sentence
				| sentenceword sentence
				| sentenceword '''
	if len(p)==2:
		p[0]=p[1]
	elif len(p)==3:
		p[0]=p[1]+p[2]
	else:
		p[0]=p[1]+p[3]

def p_sentenceword(p):
	'''sentenceword : words
	                | numbers '''
	z=re.match('[A-Za-z]+',p[1])
	p[0]=0
	if z:
		p[0]=1

def p_sections(p):
	'''sections : section sections
	            | section '''

	p[0]={'sectioncount':0,'paracount':0,'statements':[0,0,0,0],'headings':[]}
	if len(p)==2:
		p[0]['sectioncount']=1
		p[0]['paracount']=p[1]['paracount']
		p[0]['statements']=p[1]['statements']
		p[0]['headings']=[p[1]['head']]
	else:
		p[0]['sectioncount']=1 + p[2]['sectioncount']
		p[0]['paracount']=p[1]['paracount'] + p[2]['paracount']
		p[0]['statements']=add(p[1]['statements'],p[2]['statements'])
		p[0]['headings']=p[2]['headings']
		p[0]['headings'].append(p[1]['head'])

def p_section(p):
	'section : Section numbers colon headings paragraphs'
	p[0]=p[5]
	p[0]['head']='Section '+p[2]+p[3]+' '+ p[4]

def p_headings(p):
	'''headings : headingword headings
	            | headingword newlines'''
	if(p[2]==None):
		p[0] = p[1]
	else:
		p[0] = p[1] + ' '+ p[2]

def p_headingword(p):
	'''headingword : words 
	               | numbers'''
	p[0] = str(p[1])

def p_chapters(p):
	'''chapters : chapter chapters 
	            | chapter'''
	p[0]={'chaptercount':0,'paracount':0,'sectioncount':0,'statements':[0,0,0,0],'headings':[]}
	if len(p)==2:
		p[0]['chaptercount']=1
		p[0]['paracount']=p[1]['paracount']
		p[0]['sectioncount']=p[1]['sectioncount']
		p[0]['statements']=p[1]['statements']
		p[0]['headings']=[p[1]['headings']]
	else:
		p[0]['chaptercount']=1 + p[2]['chaptercount']
		p[0]['paracount']=p[1]['paracount']+p[2]['paracount']
		p[0]['sectioncount']=p[1]['sectioncount']+p[2]['sectioncount']
		p[0]['statements']=add(p[1]['statements'],p[2]['statements'])
		p[0]['headings']=p[2]['headings']
		p[0]['headings'].append(p[1]['headings'])

def p_chapter(p):
	'''chapter : chapter1
			   | chapter2 '''
	p[0]=p[1]

def p_chapter1(p):
	'''chapter1 : Chapter numbers colon headings paragraphs
			   | Chapter numbers colon headings paragraphs sections '''
	p[0]={'paracount':0,'sectioncount':0,'statements':[0,0,0,0],'headings':[]}
	if(len(p)==7):
		p[0]['sectioncount']=p[6]['sectioncount']
		p[0]['paracount']=p[5]['paracount']+p[6]['paracount']
		p[0]['statements']=add(p[5]['statements'],p[6]['statements'])
		p[0]['headings']=p[6]['headings']
		p[0]['headings'].append('Chapter '+ p[2] +p[3]+ ' '+p[4])
	else:
		p[0]['sectioncount']=0
		p[0]['paracount']=p[5]['paracount']
		p[0]['statements']=p[5]['statements']
		p[0]['headings']= ['Chapter '+ p[2] +p[3]+ ' '+p[4]]
def p_chapter2(p):
	''' chapter2 : Chapter numbers colon headings sections'''
	p[0]=p[5]
	p[5]['headings'].append('Chapter '+p[2]+p[3]+' '+p[4])

def p_thesis(p):
	'thesis : Title colon headings chapters'
	print('Title: '+p[3])
	print('Number of Chapters: ' + str(p[4]['chaptercount']))
	print('Number of Sections: ' + str(p[4]['sectioncount']))
	print('Number of Paragraphs: ' + str(p[4]['paracount']))
	print('Number of Sentences: ' + str(sum(p[4]['statements'][0:3])))
	print('Number of Words: ' + str(p[4]['statements'][3]))
	print('Number of Declarative Sentences: ' + str(p[4]['statements'][1]))
	print('Number of Exclamatory Sentences: ' + str(p[4]['statements'][0]))
	print('Number of Interrogative Sentences: ' + str(p[4]['statements'][2]))
	print('Table of Contents:')
	headings = p[4]['headings'][::-1]
	for i in headings:
		flag=0
		i=i[::-1]
		for j in i:
			if(flag==1):
				print('   '+j)
				continue
			print(j)
			flag=1
	


def p_error(p):
    print("Input Error")
    return

# Build the parser
parser = yacc.yacc()

#Input
file=open(sys.argv[1],'r')
test=file.read()
# yacc.input(test)
# print(test)
parser.parse(test,lexer)
#print(result)