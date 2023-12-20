#!/usr/bin/python3
""" Update the def do_create(self, arg): function of your command interpreter """

from datetime import datetime
import cmd
import sys
import os
import re
import uuid
from models import storage
from models.base_model import BaseModel
from models.user import User
from models.place import Place
from models.city import City
from models.state import State
from models.review import Review
from models.amenity import Amenity

class HBNBCommand(cmd.Cmd):
    """ The class represents the HBnB command interpreter."""

    # determines prompt for interactive/non-interactive modes
    prompt = '(hbnb) ' if sys.__stdin__.isatty() else ''

    classes = {
               'BaseModel': BaseModel,
	       'User': User,
	       'Place': Place,
               'State': State,
	       'City': City,
	       'Amenity': Amenity,
               'Review': Review
              }
    dot_cmds = ['all', 'count', 'show', 'destroy', 'update']
    types = {
             'number_rooms': int,
	     'number_bathrooms': int,
             'max_guest': int,
	     'price_by_night': int,
             'latitude': float,
	     'longitude': float
            }

    def prlp(self):
        """check  if isatty is false return hbnh"""
        if not sys.__stdin__.isatty():
            print('(hbnb)')

    def prcmd(self, line):
        """ Make a new format command line for a new syntax.
        """
        command = clas = idntf = _args = ''

        if not ('.' in line and '(' in line and ')' in line):
            return line

        try:
            pln = line[:]

            clas = pln[:pline.find('.')]

            command = pln[pline.find('.') + 1:pln.find('(')]
            if command not in HBNBCommand.dot_cmds:
                raise Exception

            pln = pln[pln.find('(') + 1:pln.find(')')]
            if pln:
                pln = pln.partition(', ')

                idntf = pln[0].replace('\"', '')

                pln = pln[2].strip() 
                if pln:
                    if pln[0] == '{' and pln[-1] == '}'\
                            and type(eval(pln)) is dict:
                        _args = pln
                    else:
                        _args = pln.replace(',', '')
            line = ' '.join([command, clas, idntf, _args])

        except Exception as mess:
            pass
        finally:
            return line

    def postcmd(self, stop, line):
        """Prints if isatty is false"""
        if not sys.__stdin__.isatty():
            print('(hbnb) ', end='')
        return stop

    def do_quit(self, command):
        """ Quit the HBNB DB """
        exit(0)

    def help_quit(self):
        """ Gives the help documentation to exit  """
        print("Quit  the program\n")

    def do_EOF(self, arg):
        """ Quit the prog by manipulating EOF """
        exit(0)

    def help_EOF(self):
        """ Display the help documentation in the case of  EOF """
        print("Quit the program\n")

    def emptyline(self):
        """ In case of Error returns False """
        return False

    def do_create(self, args):
        """ The funct to ceaat a class obj"""
        unkn_tr = ('id', 'created_at', 'updated_at', '__class__')
        cln = ''
        ptn = r'(?P<name>(?:[a-zA-Z]|_)(?:[a-zA-Z]|\d|_)*)'
        clm = re.match(ptn, args)
        obw = {}
        if clm is not None:
            cln = clm.group('name')
            psr = args[len(cln):].strip()
            prs = ps.split(' ')
            strp = r'(?P<t_str>"([^"]|\")*")'
            floatp = r'(?P<t_float>[-+]?\d+\.\d+)'
            intp = r'(?P<t_int>[-+]?\d+)'
            prp = '{}=({}|{}|{})'.format(
                ptn,
                strp,
                floatp,
                intp
            )
            for x in prs:
                prm = re.fullmatch(prp, x)
                if prm is not None:
                    KM = prm.group('name')
                    str_v = prm.group('t_str')
                    float_v = prm.group('t_float')
                    int_v = prm.group('t_int')
                    if float_v is not None:
                        obw[KM] = float(float_v)
                    if int_v is not None:
                        obw[KM] = int(int_v)
                    if str_v is not None:
                        obw[KM] = str_v[1:-1].replace('_', ' ')
        else:
            cln = args
        if not cln:
            print("** No class name **")
            return
        elif cln not in HBNBCommand.classes:
            print("** No class **")
            return
        if os.getenv('HBNB_TYPE_STORAGE') == 'db':
            if not hasattr(obw, 'id'):
                obw['id'] = str(uuid.uuid4())
            if not hasattr(obw, 'created_at'):
                obw['created_at'] = str(datetime.now())
            if not hasattr(obw, 'updated_at'):
                obw['updated_at'] = str(datetime.now())
            nist = HBNBCommand.classes[cln](**obw)
            nist.save()
            print(nist.id)
        else:
            nist = HBNBCommand.classes[cln]()
            for K, V in obw.items():
                if K not in unkn_tr:
                    setattr(nist, K, V)
            nist.save()
            print(nist.id)

    def help_create(self):
        """ Display the Help information for the new method """
        print("Type class creation")
        print("[Usage]: create <className>\n")

    def do_show(self, args):
        """ The output is an individual objt """
        w = args.partition(" ")
        cn = w[0]
        cidt = w[2]

        if cidt and ' ' in cidt:
            cidt = cidt.partition(' ')[0]

        if not cn:
            print("** No class name**")
            return

        if cn not in HBNBCommand.classes:
            print("** There is no class**")
            return

        if not cidt:
            print("** There is no class instance identifiar **")
            return

        K = cn + "." + cidt
        try:
            print(storage.all()[K])
        except KeyError:
            print("** no instance found **")

    def help_show(self):
        """ Help information for the show command """
        print("Shows an individual instance of a class")
        print("[Usage]: show <className> <objectId>\n")

    def do_destroy(self, args):
        """ Destroys a specified object """
        nw = args.partition(" ")
        cn = nw[0]
        cidt = nw[2]
        if cidt and ' ' in cidt:
            cidt = cidt.partition(' ')[0]

        if not cn:
            print("** class name missing **")
            return

        if cn not in HBNBCommand.classes:
            print("** class doesn't exist **")
            return

        if not cidt:
            print("** instance id missing **")
            return

        K = cn + "." + cidt

        try:
            storage.delete(storage.all()[K])
            storage.save()
        except KeyError:
            print("** There is no instance **")

    def help_destroy(self):
        """ The destroy command help """
        print(" This  class individual instance will no more exist")
        print("[Usage]: destroy <className> <objectId>\n")

    def do_all(self, args):
        """ Display the objects of a class"""
        plst = []

        if args:
            args = args.split(' ')[0]  
            if args not in HBNBCommand.classes:
                print("**There is no clase **")
                return
            for ww, v in storage.all().items():
                if ww.split('.')[0] == args:
                    plst.append(str(v))
        else:
            for ww, v in storage.all().items():
                plst.append(str(v))

        print(plst)

    def help_all(self):
        """ Displays Help information for all command """
        print("Shows Help for all objects of a class")
        print("[Usage]: all <className>\n")

    def do_count(self, args):
        """ Displays the number of class instances"""
        i = 0
        for k, v in storage.all().items():
            if args == k.split('.')[0]:
                i += 1
        print(i)

    def help_count(self):
        """ """
        print("Usage: count <class_name>")

    def do_update(self, args):
        """ Add informations to the object """
        cn = cidt = atn = atv = kwargs = ''

        args = args.partition(" ")
        if args[0]:
            cn = args[0]
        else:  
            print("** Ther is no class name **")
            return
        if cn not in HBNBCommand.classes: 
            print("** There is no class **")
            return

        args = args[2].partition(" ")
        if args[0]:
            cidt = args[0]
        else: 
            print("** No instance identifier **")
            return

        K = cn + "." + cidt

        if K not in storage.all():
            print("** There is no instance **")
            return

        if '{' in args[2] and '}' in args[2] and type(eval(args[2])) is dict:
            kwargs = eval(args[2])
            args = []  
            for k, v in kwargs.items():
                args.append(k)
                args.append(v)
        else: 
            args = args[2]
            if args and args[0] == '\"':
                st = args.find('\"', 1)
                atn = args[1:st]
                args = args[st + 1:]

            args = args.partition(' ')

            if not atn and args[0] != ' ':
                atn = args[0]
            if args[2] and args[2][0] == '\"':
                atv = args[2][1:args[2].find('\"', 1)]

            if not atv and args[2]:
                atv = args[2].partition(' ')[0]

            args = [atn, atv]

        n_dct = storage.all()[K]

        for i, atn in enumerate(args):
            if (i % 2 == 0):
                atv = args[i + 1] 
                if not atn:  
                    print("** There is no attribute name **")
                    return
                if not atv: 
                    print("** There is no value **")
                    return
                if atn in HBNBCommand.types:
                    atv = HBNBCommand.types[atn](atv)

                n_dct.__dict__.update({atn: atv})

        n_dct.save()

    def help_update(self):
        """ To update class the Help information """
        print("Updates an object of the class with new information")
        print("Usage: update <className> <id> <attName> <attVal>\n")


if __name__ == "__main__":
    HBNBCommand().cmdloop()
