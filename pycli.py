# !/usr/bin/env python
# coding=utf-8
"""
PyCLI

Este script age como um centralizador de módulos. Ao ser invocado
ele importa sobdemanda o módulo associado, ou seja, ele não carrega todos
os modulos uma vez que é chamado e permite uma resposta tão rápida quanto um
script independente.

A centralização dos scripts acaba por formar o que chamamos de CLI
ao facilitar o uso e a manuntenção do módulos associados.

@author Mauricio Quatrin Guerreiro
@version 1.2
"""
import argparse
import imp
import os

#def load_config()

def setup_on_demand(module_requested):
    fp, pathname, description = imp.find_module(module_requested, [LIB_FOLDER[0] + '/package'])
    module = imp.load_module(module_requested, fp, pathname, description)
    parser = module.setup(argparse)
    return parser

def version():
    print 'CLI ' + properties.get_version_name()

def help(modules):
    from technobox.tdns.core import properties
    print '\n' + 'Package ' + properties.get_version_name() + '\n'
    print 'Modules:'
    for module in modules:
        fp, pathname, description = imp.find_module(module, [LIB_FOLDER[0] + '/package'])
        module = imp.load_module(module, fp, pathname, description)
        parser = module.setup(argparse)
        progname = parser.prog
        for x in xrange(20 - len(parser.prog)):
            progname += " "

        print '  ' + progname + '\t' + parser.description

def main(args, extra, modules):
    if len(args.module) > 0:
        if args.module[0] in modules:
            if args.help:
                extra.append('-h')

            args = setup_on_demand(args.module.pop(0)).parse_args(args.module + extra)
            info = args.func(args)
            if info:
                print info
        else:
            print 'module ' + args.module[0] + ' not found. please, try again.'
    elif args.help:
        help(modules)
    elif args.version:
        version()
    else:
        print 'few arguments. try again.'

if __name__ == '__main__':
    LIB_FOLDER = ['/usr/local/lib/python2.7/site-packages/vendor']

    if 'scripts' in os.path.realpath('.'):
        LIB_FOLDER = [os.path.realpath('.') + '/vendor']

    try:
        fp, pathname, description = imp.find_module('package', LIB_FOLDER)
        modules = imp.load_module('package', fp, pathname, description)

    except ImportError as error:
        print error
        print 'error importing base module'
        print fp, pathname, description

    main_parser = argparse.ArgumentParser(description='CLI', prog='cli', add_help=False)
    main_parser.add_argument('module', nargs='*')
    main_parser.add_argument('-V','--version', action='store_true', help='show version')
    main_parser.add_argument('-h', '--help', action="store_true", help='show helps')
    main_parser.set_defaults(func=main)

    args, extra = main_parser.parse_known_args()
    args.func(args, extra, modules.__all__)
