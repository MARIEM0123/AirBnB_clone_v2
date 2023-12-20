#!/usr/bin/python3
""" The module to test cmd interpreterof the console.
"""
import MySQLdb
import json
import os
from unittest.mock import patch
import sqlalchemy
import unittest
from io import StringIO
from console import HBNBCommand
from models.base_model import BaseModel
from models.user import User
from tests import clear_stream
from models import storage

class TestHBNBCommand(unittest.TestCase):
    """ The first est class for the HBNBCommand class.
    """
    @unittest.skipIf(
        os.getenv('HBNB_TYPE_STORAGE') == 'db', 'FileStorage test')
    def test_fs_create(self):
        with patch('sys.stdout', new=StringIO()) as c:
            cs = HBNBCommand()
            cs.onecmd('create City name="California"')
            mdl_id = c.getvalue().strip()
            clear_stream(c)
            self.assertIn('City.{}'.format(mdl_id), storage.all().keys())
            cs.onecmd('show City {}'.format(mdl_id))
            self.assertIn("'name': 'California'", c.getvalue().strip())
            clear_stream(c)
            cs.onecmd('create User name="MARIEM" age=32 height=1.56')
            mdl_id = cout.getvalue().strip()
            self.assertIn('User.{}'.format(mdl_id), storage.all().keys())
            clear_stream(c)
            cs.onecmd('show User {}'.format(mdl_id))
            self.assertIn("'name': 'MARIEM'", c.getvalue().strip())
            self.assertIn("'age': 32", c.getvalue().strip())
            self.assertIn("'height': 1.56", c.getvalue().strip())

    @unittest.skipIf(
        os.getenv('HBNB_TYPE_STORAGE') != 'db', 'DBStorage test')
    def test_db_create(self):
        """A new test fot the DB storagee.
        """
        with patch('sys.stdout', new=StringIO()) as c:
            cs = HBNBCommand()
            with self.assertRaises(sqlalchemy.exc.OperationalError):
                cs.onecmd('create User')
            clear_stream(c)
            cs.onecmd('create User email="MARIEM0123@gmail.com" password="123"')
            mdl_id = c.getvalue().strip()
            dbc = MySQLdb.connect(
                host=os.getenv('HBNB_MYSQL_HOST'),
                port=1234,
                user=os.getenv('HBNB_MYSQL_USER'),
                passwd=os.getenv('HBNB_MYSQL_PWD'),
                db=os.getenv('HBNB_MYSQL_DB')
            )
            cursor = dbc.cursor()
            cursor.execute('SELECT * FROM users WHERE id="{}"'.format(mdl_id))
            rt = cursor.fetchone()
            self.assertTrue(rt is not None)
            self.assertIn('MARIEM0123@gmail.com', rt)
            self.assertIn('123', rt)
            cursor.close()
            dbc.close()

    @unittest.skipIf(
        os.getenv('HBNB_TYPE_STORAGE') != 'db', 'DBStorage test')
    def test_db_show(self):
        """ New test for the database storage.
        """
        with patch('sys.stdout', new=StringIO()) as c:
            cs = HBNBCommand()
            obj = User(email="MARIEM0123@gmail.com", password="123")
            dbc = MySQLdb.connect(
                host=os.getenv('HBNB_MYSQL_HOST'),
                port=1234,
                user=os.getenv('HBNB_MYSQL_USER'),
                passwd=os.getenv('HBNB_MYSQL_PWD'),
                db=os.getenv('HBNB_MYSQL_DB')
            )
            crs = dbc.cursor()
            crs.execute('SELECT * FROM users WHERE id="{}"'.format(obj.id))
            rt = crs.fetchone()
            self.assertTrue(rt is None)
            cs.onecmd('show User {}'.format(obj.id))
            self.assertEqual(
                c.getvalue().strip(),
                '** There is no instance **'
            )
            obj.save()
            dbc = MySQLdb.connect(
                host=os.getenv('HBNB_MYSQL_HOST'),
                port=1234,
                user=os.getenv('HBNB_MYSQL_USER'),
                passwd=os.getenv('HBNB_MYSQL_PWD'),
                db=os.getenv('HBNB_MYSQL_DB')
            )
            crs = dbc.cursor()
            crs.execute('SELECT * FROM users WHERE id="{}"'.format(obj.id))
            clear_stream(cout)
            cs.onecmd('show User {}'.format(obj.id))
            rt = crs.fetchone()
            self.assertTrue(rt is not None)
            self.assertIn('MARIEM0123@gmail.com', rt)
            self.assertIn('123', rt)
            self.assertIn('MARIEM0123@gmail.com', c.getvalue())
            self.assertIn('123', c.getvalue())
            crs.close()
            dbc.close()

    @unittest.skipIf(
        os.getenv('HBNB_TYPE_STORAGE') != 'db', 'DBStorage test')
    def test_db_count(self):
        """New test of the count for the database storage.
        """
        with patch('sys.stdout', new=StringIO()) as c:
            cs = HBNBCommand()
            dbc = MySQLdb.connect(
                host=os.getenv('HBNB_MYSQL_HOST'),
                port=1234,
                user=os.getenv('HBNB_MYSQL_USER'),
                passwd=os.getenv('HBNB_MYSQL_PWD'),
                db=os.getenv('HBNB_MYSQL_DB')
            )
            crs = dbc.cursor()
            crs.execute('SELECT COUNT(*) FROM states;')
            res = crs.fetchone()
            pvc = int(res[0])
            cs.onecmd('create State name="Enugu"')
            clear_stream(c)
            cs.onecmd('count State')
            cnt = c.getvalue().strip()
            self.assertEqual(int(cnt), pvc + 1)
            clear_stream(c)
            cs.onecmd('count State')
            crs.close()
            dbc.close()
