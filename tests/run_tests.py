#!/usr/bin/python2

import sys, os

#-------------------------------------------------------------------------------
# Change here, if needed

QT_FLAGS = "-I /usr/include/qt/ -fPIC"
#-------------------------------------------------------------------------------
# Global variables

_compiler_comand = "clang++ -std=c++11 -Wno-unused-value -Qunused-arguments -Xclang -load -Xclang ClangMoreWarningsPlugin.so -Xclang -add-plugin -Xclang more-warnings -c *.cpp " + QT_FLAGS + " -Xclang -plugin-arg-more-warnings -Xclang "
_dump_ast_command = "clang++ -std=c++11 -fsyntax-only -Xclang -ast-dump -fno-color-diagnostics -c *.cpp " + QT_FLAGS
_dump_ast = "--dump-ast" in sys.argv


#-------------------------------------------------------------------------------
# utility functions
def print_usage():
    print "Usage:"
    print sys.argv[0] + " [--help] [--dump-ast] [check1,check2,check3]"
    print
    print "Without any check supplied, all checks will be run."
    print "--dump-ast is provided for debugging purposes.\n"

def run_command(cmd):
    if os.system(cmd) != 0:
        return False
    return True

def run_command2(cmd):
    return os.popen(cmd).readlines()

def files_are_equal(file1, file2):
    try:
        f = open(file1, 'r')
        lines1 = f.readlines()
        f.close()

        f = open(file2, 'r')
        lines2 = f.readlines()
        f.close()

        return lines1 == lines2
    except:
        return False

def get_check_list():
    return filter(lambda entry: os.path.isdir(entry), os.listdir("."))

def print_differences(file1, file2):
    return run_command("diff -Naur test.expected test.output")

def run_check_unit_tests(check):
    if not run_command(_compiler_comand + check + " &> compile.output"):
        print "[FAIL] " + check + " (Failed to build test. Check " + check + "/compile.output for details)"
        print
        return False
    os.system("grep \"warning:\" compile.output &> test.output")

    if files_are_equal("test.expected", "test.output"):
        print "[OK]   " + check
    else:
        print "[FAIL] " + check
        if not print_differences("test.expected", "test.output"):
            return False

    return True

def dump_ast(check):
    run_command(_dump_ast_command + " > ast_dump.output")
#-------------------------------------------------------------------------------
# main

if "--help" in sys.argv:
    print_usage()
    sys.exit(0)

args = sys.argv[1:]
if _dump_ast:
    del(args[args.index("--dump-ast")])


all_checks = get_check_list()
requested_checks = args

for check in requested_checks:
    if check not in all_checks:
        print "Unknown check: " + check
        print
        sys.exit(-1)

if not requested_checks:
    requested_checks = all_checks

for check in requested_checks:
    os.chdir(check)
    if _dump_ast:
        dump_ast(check)
    else:
        run_check_unit_tests(check)

    os.chdir("..")
