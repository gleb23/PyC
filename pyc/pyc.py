import os
import sys

from pyc.errs import CompileError, RuntimeErr
from pyc.syntan import Syntan


__author__ = 'hlib'

source = '''
{
int factorial(int n) {
    int[3] a;
    if (n == 2 || n == 0 || n ==1) {
        int c = 0;
        while (c < 2) {
            a[c] = 1;
            c = c + 1;
        }
        a[c] = c;
    }
    //print a[0];
    //print a[1];
    //print a[2];

    if (n == 0) {
        return a[10];
    } else if (n == 1){
        return a[n];
    } else if (n == 2){
        return a[n];
    } else {
        return n * factorial(n - 1);
    }
    return n;
}
int k =  0;
while (k != 100) {
    int k =  factorial(get());
    print "result:";
    //print k;
    put(k);
}
}
'''
# source = '''
# int m(int[4] a, int b) {
#     return a[b];
# }
# int[4] a;
# a[0] = 0;
# a[1] = 1;
# a[2] = 2;
# a[3] = 3;
# int b = m(a, 2);
# print b;
# '''
# source = '''
# void m() {
#     int a = 2;
#     int countercountercounter = 1;
#     while (a > 0) {
#         if (a < 3) {
#             print "3";
#             if (a == 2) {
#                 print "2";
#                 a = 0;
#             }
#             if (a < 1) {
#                 print "1";
#             }
#         }
#         if (countercountercounter == 0) {
#             a = 0;
#             print "yes";
#         }
#         if (countercountercounter) {
#             countercountercounter = false;
#             a = 1;
#             print "yes";
#         }
#     }
# }
# int a = 0;
# m();
# '''
# source = '''
# void f(int[2] m) {
#     print m[0];
#     print m[1];
# }
# int[2] m;
# int i = 0;
# while (i<2) {
#     m[i] = i;
#     i = i + 1;
# }
# f(m);
# '''

# source = '''
# {
# int f(int n) {
#     if (n == 13) {
#         return 0;
#     }
#     return n * n;
# }
# print f(3) + f(2);}
# '''

#TODO add param in out

class Executor(object):
    def __init__(self, source):
        self.source = source

    def execute(self):
        try:
            flowTree = Syntan(self.source).parse()
            for instruction in flowTree.block.instructions:
                instruction.execute()
        except CompileError, ex:
            print "PyC Error!!!"
            print ex
        except RuntimeErr, ex:
            print "PyC Error!!!"
            print ex
        except RuntimeError, ex:
            print "PyC Error!!!"
            print ex
        except BaseException, ex:
            print "PyC Error!!!"
            print ex
        print '\npress any key...\n'
        raw_input()


    def seek_errors(self):
        try:
            flowTree = Syntan(self.source).parse()
        except:
            pass

try:
    if len(sys.argv) > 1:
        file_name = sys.argv[1]
        file = open(file_name, 'r')
        source = file.read()

    Executor(source).execute()
except IOError:
    print 'No such file!!!'