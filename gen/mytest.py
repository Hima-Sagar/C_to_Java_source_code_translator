import sys
import re
#from inspect import signature
from antlr4 import *
from CLexer import CLexer
#from CListener import CListener
from CParser import CParser
from CVisitor import CVisitor


class MyCVisitor(CVisitor):
    pass
    '''  def __init__(self):
        self.VarList=[]

    def getVarList(self):
        return self.VarList

    def visitDirectDeclarator(self, ctx):
        if(ctx.getChildCount()==1):
            self.VarList.append(ctx.getText())
            '''

class MyCVisitor2(CVisitor):
    def __init__(self):
        self.nodeCounter = 1
        self.textdict={}
        self.crude_cfg = ""
        self.VarList = []
        self.comandArguments = 0
        self.objectCreated = 0
        self.indentation = 1
    # dictionary={
    #     "int main()":""
    # }
    def printIndentation(self):
        n=self.indentation
        f = open("output.java", "a+")
        while n>0:
            f.write("\t")
            n-=1
        f.close()


    def getComandArguments(self):
        return self.comandArguments
    def getCrudeCfg(self):
        return self.crude_cfg

    def getdict(self):
        return self.textdict

    def getVarList(self):
        return self.VarList


#### RETURN ;
    def visitJumpStatement(self, ctx):
        st=ctx.getText()
        st = st.replace('return', 'return ')
        st = st.replace('(unsignedint)', '')
        st = st.replace('(int)', '')
        self.printIndentation()
        f = open("output.java", "a+")
        f.write(st + "\n")
        f.close()


#### FOR VARIABLE DECLARATIONS OR DEFINING(ASSIGNING A VALUE DURING DECLARATION)
    def visitDeclaration(self, ctx):
        # if(ctx.children[0].getText()=="int"):
        # print(type(ctx.getText()))

        # if(ctx.getText().find("(")!= -1 and self.objectCreated==0):
        #     self.objectCreated = 1
        #     f = open("output.java", "a+")
        #     f.write("Test testObj = new Test();\n")
        #     f.close()
        ##integrated the function declaration and definations and removed the declaration
        if(ctx.getText().find("=")== -1 and ctx.getText().find(");")!= -1):
            pass
        else :
            st=ctx.children[0].getText()
            st = st.replace('char*', 'String ')
            st = st.replace('unsignedint', 'int ')
            self.printIndentation()
            f = open("output.java", "a+")
            f.write(st +" ")
            f.close()
            self.visitChildren(ctx)
            f = open("output.java", "a+")
            f.write(ctx.children[2].getText() + " \n" )
            f.close()

    def visitInitDeclarator(self, ctx):
        if(ctx.getChildCount()>1):

            f = open("output.java", "a+")
            f.write(ctx.getText() + " ")
            f.close()


        else:
            if(ctx.getText().find("(")==-1):
                f = open("output.java", "a+")
                f.write(ctx.getText() + " ")
                f.close()


    def visitInitDeclaratorList(self, ctx):
        if(ctx.getChildCount()>1):
            self.visit(ctx.children[0])
            f = open("output.java", "a+")
            f.write(ctx.children[1].getText() + " ")
            f.close()
            self.visit(ctx.children[2])
        else:
            self.visitChildren(ctx)


#### PRINTF() , ALL OTHER ASSIGNMENT STATEMENTS , VOID FUNCTION CALLS
    def visitExpressionStatement(self, ctx):
        if (ctx.children[1].getText() == ";" and ctx.children[0].getText()[0:6] == "printf"):
            # print(ctx.children[0].getText())
            st=ctx.children[0].getText()[8:]
            i=0

            self.printIndentation()

            if(st.find('%d',i)!=-1 or st.find('%f',i)!=-1 or st.find('%c',i)!=-1 or st.find('%s',i)!=-1 or st.find('%u',i)!=-1 or st.find('%ld',i)!=-1 ):
                f = open("output.java", "a+")
                f.write('System.out.println(')
                f.close()
                comma=st.find('",')+2

                while(st.find('%d',i)!=-1 or st.find('%f',i)!=-1 or st.find('%c',i)!=-1 or st.find('%s',i)!=-1 or st.find('%u',i)!=-1 or st.find('%ld',i)!=-1 ):
                    a=[]
                    if st.find('%d',i)!=-1 :
                        a.append(st.find('%d',i))
                    if st.find('%f',i)!=-1 :
                        a.append(st.find('%f',i))
                    if st.find('%c',i)!=-1 :
                        a.append(st.find('%c',i))
                    if st.find('%s',i)!=-1 :
                        a.append(st.find('%s',i))
                    if st.find('%u',i)!=-1 :
                        a.append(st.find('%u',i))
                    if st.find('%ld', i) != -1:
                        a.append(st.find('%ld', i))
                    m=min(a)
                    if(st.find(',',comma)!=-1):
                        next =st.find(',',comma)
                    else:
                        next = st.find(')', comma)

                    f = open("output.java", "a+")

                    if(st[i:m]==""):
                        f.write(st[comma:next])
                    else:
                        f.write('"'+st[i:m]+'"+'+st[comma:next])
                    f.close()
                    i = m + 2
                    comma =next+1
                f = open("output.java", "a+")
                f.write(');\n')
                f.close()

            else:
                f = open("output.java", "a+")
                f.write("System.out.println" + ctx.children[0].getText()[6:] + ";\n")
                f.close()
        else:
            self.printIndentation()
            self.visitChildren(ctx)
            f = open("output.java", "a+")
            f.write(ctx.children[1].getText() + " \n")
            f.close()

    def visitExpression(self, ctx):
        if (ctx.getChildCount() > 1):
            self.visit(ctx.children[0])
            f = open("output.java", "a+")
            f.write(ctx.children[1].getText() + " ")
            f.close()
            self.visit(ctx.children[2])
        else:
            self.visitChildren(ctx)

    def visitAssignmentExpression(self, ctx):

        f = open("output.java", "a+")
        f.write(ctx.getText() + " ")
        f.close()



#### IF ELSE STATEMENTS
    def visitSelectionStatement(self, ctx):
        #if(
        self.printIndentation()
        f = open("output.java", "a+")
        f.write(ctx.children[0].getText() + ctx.children[1].getText() +" ")
        f.close()
        st=ctx.children[2].getText()
        st = st.replace('(unsignedint)', '')
        st = st.replace('(int)', '')
        st = st.replace('unsignedint', 'int ')
        st=st.replace('int','int ')

        #boolen expression ){
        f = open("output.java", "a+")
        f.write(st + ctx.children[3].getText() + "{ \n" )
        f.close()
        #visiting body of if

        self.indentation += 1
        self.visit(ctx.children[4])
        self.indentation -= 1
        # }
        self.printIndentation()
        f = open("output.java", "a+")
        f.write("}\n")
        f.close()

        if(ctx.getChildCount()==7):
            # else{
            self.printIndentation()
            f = open("output.java", "a+")
            f.write( ctx.children[5].getText() + "{ " + "\n")
            f.close()

            #visiting else body
            self.indentation += 1
            self.visit(ctx.children[6])
            self.indentation -= 1
            #}

            self.printIndentation()
            f = open("output.java", "a+")
            f.write("}\n")
            f.close()

#### LOOPS FOR ,WHILE ,DO WHILE
    def visitIterationStatement(self, ctx):
        self.printIndentation()
        if (ctx.children[0].getText() == "while" or ctx.children[0].getText() == "for" ):
            f = open("output.java", "a+")
            f.write(ctx.children[0].getText() + ctx.children[1].getText() + " ")
            f.close()
            st = ctx.children[2].getText()

            st = st.replace('(unsignedint)', '')
            st = st.replace('(int)', '')
            st = st.replace('unsignedint', 'int ')
            st=st.replace('int','int ')


            # boolen expression ){
            f = open("output.java", "a+")
            f.write(st + ctx.children[3].getText() + "{ \n")
            f.close()
            # visiting body of if
            self.indentation += 1
            self.visit(ctx.children[4])
            self.indentation -= 1
            # }

            self.printIndentation()
            f = open("output.java", "a+")
            f.write("} \n")
            f.close()


        if (ctx.children[0].getText() == "do"):
            f = open("output.java", "a+")
            f.write(ctx.children[0].getText() + " { \n")
            f.close()
            self.indentation += 1
            self.visit(ctx.children[1])
            self.indentation -= 1


            self.printIndentation()
            f = open("output.java", "a+")
            f.write('} ')
            f.close()
            f = open("output.java", "a+")
            f.write(ctx.children[2].getText() + ctx.children[3].getText() + " ")
            f.close()
            ss = ctx.children[4].getText()
            #
            ss = ss.replace('(unsignedint)', '')
            ss = ss.replace('(int)', '')
            ss = ss.replace('unsignedint', '')
            ss=ss.replace('int','')

            # boolen expression ){
            f = open("output.java", "a+")
            f.write(ss + ctx.children[5].getText() + "; \n")
            f.close()


#### FUNCTIONS DEFINITIONS
    def visitFunctionDefinition(self, ctx):
        self.printIndentation()
        f = open("output.java", "a+")
        f.write('public static ')
        f.close()
        if(ctx.children[1].children[0].children[0].getText()=='main'):
            f = open("output.java", "a+")
            f.write(' void main(String[] args) { \n')
            f.close()

        else:
            f = open("output.java", "a+")
            f.write(ctx.children[0].getText() +" ")
            f.close()
            st=ctx.children[1].getText()
            st = st.replace('(unsignedint)', '')
            st = st.replace('(int)', '')
            st = st.replace('unsignedint', 'int ')
            st = st.replace('int', 'int ')
            st = st.replace('float', 'float ')
            st = st.replace('double', 'double ')
            st = st.replace('short', 'short ')
            st = st.replace('long', 'long ')
            st = st.replace('char', 'char ')
            st = st.replace('char*', 'String ')
            f = open("output.java", "a+")
            f.write(st+'{ \n')
            f.close()
        self.indentation += 1
        self.visit(ctx.children[2])
        self.indentation -= 1

        self.printIndentation()
        f = open("output.java", "a+")
        f.write('} \n')
        f.close()


def main(argv):
    input = FileStream(argv[1])
    lexer = CLexer(input)

    stream = CommonTokenStream(lexer)
    parser = CParser(stream)
    tree = parser.compilationUnit()
    # print(tree)
    ast = tree.toStringTree(recog=parser)
    # print(ast)



#### CLASS NAME {
    f = open("output.java", "w+")
    f.write("public class Test {\n")
    f.close()
    v2 = MyCVisitor2()
    v2.visit(tree)
#     HERE WE START VISITING THE NODES OF THE VISITOR

#### }

    f = open("output.java", "a+")
    f.write("}")
    f.close()


if __name__ == '__main__':
    main(sys.argv)
