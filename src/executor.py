from src.errs import UnknownIdentifierError, UnexpectedIdentifierError
from src.syntan import Syntan

__author__ = 'gleb23'

source = '''
{
int a = 32;
{
// int b = 0; // this causes problems count this new line
while (a) {
a = a - 1;
print a;
}
string s = "hello, world!";
print s;
}
}

'''

class Executor(object):
    def __init__(self, source):
        self.source = source
    def execute(self):
        try:
            print '--------------- ----- -----------------'
            flowTree = Syntan(self.source).parse()
            print '--------------- ----- -----------------'
            for instruction in flowTree.block.instructions:
                instruction.execute()
        except UnknownIdentifierError, ex:
            print "PyC Error!!!"
            print ex
        except UnexpectedIdentifierError, ex:
            print "PyC Error!!!"
            print ex

Executor(source).execute()