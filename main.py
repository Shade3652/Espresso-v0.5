tokens = []
num = ""
point = False
string = ""
binops = []
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
    "void",     #Void function type.          Usage: void x(args):
    "fun",      #Function declaration.        Usage: fun type x(args):
    "class",    #Class declaration      Usage: class x:
    "return",   #Returns a value from a function.      Usage: return ______. If used in a void function, it will return nothing. If used outside of a function, it will end the program.
    "static",   #Global variable declaration. Will make any variable with that name share the same variable (As static variables do).       Usage: static type x = ______
    "break"    #Breaks the current loop.       Usage: break NOTE THAT IF IT IS USED IN A FUNCTION, IT WILL RETURN NOTHING (LIKE VOID)
    "continue"  #Skips the current iteration of the loop.      Usage: continue
    "while"     #While loop.      Usage: while ______:
    "for"       #For loop.        Usage: for ______:

]



class Token:
    def __init__(self, type, value = None):
        global last
        self.type = type
        self.value = value
        if last != "RPAR":
            tokens.append(self)
        else:
            tokens.insert(len(tokens)-1, self)
        last = type


class Lexer:
    def lex(text):
        global tokens, point, num, string
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
            elif i in "1234567890.":
                if i == ".":
                    if point:
                        break       #To-Do: Add error handling
                    else:
                        point = True

                num = num + i

            elif i in "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ":
                string = string + i

            if not i in "1234567890.":
                Lexer.numChk()

            if not i in "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ":
                Lexer.strChk()



    def numChk():     #Actually adds the numbers to the tokens list. Last flag because it needs to be ran one time after the lexer loop just in case the last character is a number
            global point, num, tokens
            if point:       #Checks to see if the number is a float or an int and sets type accoringly
                Token("FLOAT", num)
            else:
                Token("INT", num)
                
            point = False
            num = ""

    def strChk():
        global string, tokens
        if len(string) > 1:
            Token("CHRSTR", string)
        else:
            Token("CHAR", string)
        string = ""

    def finalize():
        Lexer.lex(text)
        if text[len(text) - 1] in "1234567890":
            Lexer.numChk()

        if text[len(text) - 1] in "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ":
            Lexer.strChk()
        done = False
        while not done:
            done = True
            for i in tokens:
                if (i.type == "INT" or i.type == "CHARSTR" or i.type == "CHAR") and i.value == "":
                    tokens.remove(i)
                    done = False


class Parser:
    def parse():
        for i in tokens:
            if i.type == "RPAR":
                spot = tokens.index(i)
                tokens.pop(spot)
                tokens.insert(spot, Token("RPAR"))
                

#text = input("Espresso > ")
text = "(321 + 3) / ((6 + 4) - 69.420)"

Lexer.finalize()

for i in tokens:
    if i.type == "NEST":
        for j in i.value:
            print(j.type, j.value)
            print(j.type, j.value)
    else:
        print(i.type, i.value)
#print("__________________________________")
#for i in binops:
    #print(i.lop.value, i.op.type, i.rop.value)