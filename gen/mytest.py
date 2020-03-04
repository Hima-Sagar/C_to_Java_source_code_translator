import sys
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

    # dictionary={
    #     "int main()":""
    # }
    def getComandArguments(self):
        return self.comandArguments
    def getCrudeCfg(self):
        return self.crude_cfg

    def getdict(self):
        return self.textdict

    def getVarList(self):
        return self.VarList


#### INT MAIN(){ }

    def visitTranslationUnit(self, ctx):    # functions
        # print(dir(ctx))
        if(ctx.getChildCount() > 1):
            pass
        else:
            # print("***")
            #### To find whether there are command line arguments
            if (ctx.children[0].children[0].children[1].children[0].getChildCount() > 3):
                self.comandArguments=1

            else:
                self.comandArguments=0

                f=open("output.java","a+")
                # f.write("hiiii\n")
                if(ctx.children[0].children[0].children[0].getText()=="int" or ctx.children[0].children[0].children[0].getText()=="void" and ctx.children[0].children[0].children[1].children[0].children[0].getText()=="main"):
                    f.write("\tpublic static void main")

                if(ctx.children[0].children[0].children[1].children[0].children[1].getText()=="("):
                    f.write("(")
                if (ctx.children[0].children[0].children[1].children[0].children[2].getText() == ")"):
                    f.write(")")
                if (ctx.children[0].children[0].children[2].children[0].getText() == "{"):
                    f.write("{\n")

                f.close()
                self.visit(ctx.children[0])
                f=open("output.java","a+")
                if (ctx.children[0].children[0].children[2].children[2].getText() == "}"):
                    f.write("\t}\n")
                f.close()
         # print(ctx.getText())


#### RETURN ;
    def visitCompoundStatement(self,ctx):

        self.visit(ctx.children[1])
        if(ctx.children[1].children[1].children[0].children[0].children[0].getText()=="return" and ctx.children[1].children[1].children[0].children[0].children[2].getText()==";" and ctx.children[1].children[1].children[0].children[0].children[1].getText()!=""):
            f=open("output.java","a+")
            f.write("\t\treturn;\n")
            f.close()

    # def visitBlockItemList(self,ctx):
    #     # print(ctx.children[1].getText())
    #     n = ctx.getChildCount()
    #     for i in range(n):
    #         self.visit(ctx.children[i])
    #
    #     # self.visitChildren(ctx)


#### PRINTF();
    def visitExpressionStatement(self,ctx):
        if(ctx.children[1].getText()==";" and ctx.children[0].getText()[0:6]=="printf"):
            # print(ctx.children[0].getText())
            f = open("output.java", "a+")
            f.write("\t\tSystem.out.print"+ctx.children[0].getText()[6:]+";\n")
            f.close()

#####IMPORTANT UNABLE TO VISIT THIS METHOD OF TREE.
    # def visitPostfixExpression(self,ctx):

    #     if(ctx.children[0].getText()=="printf" and ctx.children[1].getText()=="(" and ctx.children[3].getText()==")" ):
    #         # self.visit(ctx.children[0])
    #         print(ctx.children[2].getText())
    #         f = open("output.java", "a+")
    #         f.write("System.out.print("+ctx.children[2].getText()+");\n")
    #         f.close()


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
    f.write("public class DemoTranslation {\n")
    f.close()
    v2 = MyCVisitor2()
    v2.visit(tree)

#### }

    f = open("output.java", "a+")
    f.write("}")



if __name__ == '__main__':
    main(sys.argv)
