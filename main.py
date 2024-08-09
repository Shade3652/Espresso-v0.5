tokens = []
num = ""
point = False
string = ""
parenSets = []
ast = []
last = ""

keywords = [
    "log",      #Prints to console.     Usage: log("Hello, World!")
    "if",       #Checks if the given boolean is true.       Usage: if ______:
    "contains", #Checks if the given string contains the given substring.      Usage: contains("Hello, World!", "Hello")
    "else",     #What to execute if the last valid if statement is false.      Usage: else:
    "int",      #Intiger variable type.       Usage: int x = ______. NOTE THAT ANY VARIABLE THAT IS USED TO DEFINE A FUNCTION WILL BE IT'S RETURN TYPE
    "str",      #String variable type.        Usage: str x = "______"
    "bool",     #Boolean variable type.       Usage: bool x = True/False
    "float",    #Float variable type.         Usage: float x = ______
    "char,"     #Character variable type.     Usage: char x = "______"
    "none"      #None variable type.          Usage: none x = None, or just none x. Is the only variable that can be re-assigned to any type
    "void",     #Void function type.          Usage: void x(args):
    "fun",      #Function declaration.        Usage: fun type x(args):
    "class",    #Class declaration      Usage: class x:
    "return",   #Returns a value from a function.      Usage: return ______. If used in a void function, it will return nothing. If used outside of a function, it will end the program.
    "static",   #Global variable declaration. Will make any variable with that name share the same variable (As static variables do).       Usage: static type x = ______
    "break"     #Breaks the current loop.       Usage: break. NOTE THAT IF IT IS USED IN A FUNCTION, IT WILL RETURN NOTHING (LIKE VOID)
    "continue"  #Skips the current iteration of the loop.      Usage: continue
    "while"     #While loop.      Usage: while ______:
    "for"       #For loop.        Usage: for ______:
    "and"       #Boolean AND operator.        Usage: ______ and ______
    "or"        #Boolean OR operator.         Usage: ______ or ______
    "not"       #Boolean NOT operator.        Usage: not ______

]


class Token:        #Used to define a new token. It gets assigned a type, a value (if any), and it fixes a bug where right parentheses are added one spot 
    def __init__(self, type, value = None, add = True):  #below where they should be (ex. text: "(6+3)"), tokens would be: "(", "6", "+", ")","3" instead of "(", "6", "+", "3", ")"
        global last
        self.type = type
        self.value = value
        if (last == "RPAR" and add) or ((last == "PLUS" or last == "MINUS" or last == "MUL" or last == "DIV" or last == "MOD" or last == "EQUAL") and (self.type == "INT") and add):
            tokens.insert(len(tokens)-1, self)
        elif add:
            tokens.append(self)
        last = type


class Lexer:            #Used to define the lexer. Tokenizes the Numbers, Strings of text, and special characters
    def lex():
        global tokens, point, num, string, text
        point = False
        num = ""
        string = ""
        for i in text:
            if i == "+":
                Token("PLUS")
            elif i == "-":
                Token("MINUS")
            elif i == "-":
                Token("MINUS")
            elif i == "*":
                Token("MUL")
            elif i == "/":
                Token("DIV")
            elif i == "%":
                Token("MOD")
            elif i == "(":
                Token("LPAR")
            elif i == ")":
                Token("RPAR")
            elif i == '"':
                Token("DQUO")
            elif i == "'":
                Token("SQUO")
            elif i == "=":
                Token("EQUAL")
            elif i in "1234567890.":
                if i == ".":
                    if point:
                        break       #To-Do: Add error handling (Number with 2 decimal points)
                    else:
                        point = True

                num = num + i

            elif i in "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ":
                string = string + i

            if not i in "1234567890.":
                Lexer.numChk()

            if not i in "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ":
                Lexer.strChk()



    def numChk():     #Actually adds the numbers to the tokens list.
            global point, num, tokens
            if point:       #Checks to see if the number is a float or an int and sets type accoringly
                Token("FLOAT", num)
            else:
                Token("INT", num)
                
            point = False
            num = ""

    def strChk():       #just differentiates between a string of characters and a single character
        global string, tokens
        if len(string) > 1:
            Token("CHARSTR", string)
        else:
            Token("CHAR", string)
        string = ""

    def finalize():     #Fixes glitched tokens, like chars, strings, or ints that have no value. This is a bug that I decided to not fix, but rather work around
        global text, tokens #(The bug being that the num and string checker is called every token, no matter what. I noticed this after I had already implemeted this fix, so oops :D).
        if text[len(text) - 1] in "1234567890":     #Checks last token if it was an int because theres a bug that idk how to fix | 1 DAY LATER: Figured out how to fix it but won't
            Lexer.numChk()

        if text[len(text) - 1] in "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ": #Checks last token if it was a char/string because theres a bug that idk how to fix
            Lexer.strChk()
        done = False
        while not done:
            done = True
            for i in tokens:
                if (i.type == "INT" or i.type == "CHARSTR" or i.type == "CHAR") and i.value == "":
                    tokens.remove(i)
                    done = False


class Parser:
    def preparse():
        global parenSets
        parens = []
        looking = False     #This variable is used only for error checking :D

        for i in tokens:
            if i.type == "LPAR":        #Adds every left parenthesis to a list so that if a right parenthesis is found, it can be paired with the last left parenthesis
                parens.append(i)        #AND it can detect if a parenthesis set si inside another parenthesis set
                looking = True
            elif i.type == "RPAR":      #Pairs the right parenthesis with the last left parenthesis
                looking = False 
                if not len(parens) == 0:
                    templist = [parens[len(parens)-1], i]
                else:
                    pass        #To-Do: Add error handling (RPAR with no LPAR before it.)
                    break

                parenSets.append(Token("AST", value = templist, add = False))       #Adds the actual stuff in the parenthesis to a list in order beacuse doing that garuntees that if you 
                parens.pop(len(parens)-1)       # execute the AST's from the beggining, you wont have to evaluate another AST, and adds pointers to tokens list to keep this style of
                #execution. Also, it supports endless nesting of parenthesis sets and dynamic placement of AST's and variables.

        if looking:
            pass #To-Do: Add error handling (LPAR with no RPAR after it.)
        looking = False
                                                    #Just finished adding documentation to preparse Jesus Christ I hate adding documentation. I always right the entire class and THEN
                                                    #document it. I should probably do it as I go along..

    def parse():
        global ast, text        #Guess what this does :D
        count = 0
        for i in range(text.count("(")):        #Makes this be re-executed for every parenthesis set. While just once DOES document all of the parenthesis bounds, those get 
            tempAst = []                        #messed up once the AST's are added to the tokens list and the parenthesis sets are removed. This is why I have to re-execute this

            insert = tokens.index(parenSets[0].value[0])        #Gets the index of the LPAR that the script is working on because I can't just tokens.index(parenSets[0].value[0]) because
                                                                #It gets deleted when the AST's are added to the tokens list.
            for i in range(tokens.index(parenSets[0].value[0]), tokens.index(parenSets[0].value[1]) + 1):
                tempAst.append(tokens[insert])       #Setting up the AST
                tokens.remove(tokens[insert])
            
            ast.append(Token("AST", value = tempAst, add = False))      #Adding the AST to the list of AST's
            tokens.insert(insert, Token("ASTPOINTER", len(ast) - 1))    #Adding a pointer to the AST in the tokens list so that it can be executed easier
                
            parenSets.pop(0)        #Removing the parenthesis set from the list of parenthesis sets
            count = count + 1       #Counting how many parenthesis sets there are so that the script knows how much to bugfix the tokens list end

        for i in range(count):
            tokens.pop(len(tokens)-1)       #Removing tokens that are kinda bugged and shouldn;t be there
                
def finalize():         #Just replaces some CHARSTR's and CHAR's with KEYWORD's if they are a keyword so as little work has to be done by the runtime
    global tokens, keywords, ast
    for i in tokens:
        if (i.type == "CHARSTR" or i.type == "CHAR") and (i.value in keywords):
            i.type = "KEYWORD"

    for i in ast:
        for j in i.value:
            if (j.type == "CHARSTR" or j.type == "CHAR") and (j.value in keywords):
                j.type = "KEYWORD"


#text = input("Espresso > ")
text = "(if 321 + 3) / 6 + ((6 + 4) - 69.420)"        #THIS IS THE CODE THAT ACTUALLY GETS EXECUTED   

Lexer.lex()
Lexer.finalize()
Parser.preparse()
Parser.parse()
finalize()


for i in tokens:        #Just prints out the tokens list for debugging and development purposes
    print(i.type, i.value)

print("______________________")

for i in ast:           #Just prints out the AST's for debugging and development purposes
    for j in i.value:
        print(j.type, j.value)
    print("______________________")