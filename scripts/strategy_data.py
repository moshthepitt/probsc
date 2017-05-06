#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This file has been automatically generated.
# Instead of changing it, create a file called import_helper.py
# and put there a class called ImportHelper(object) in it.
#
# This class will be specially casted so that instead of extending object,
# it will actually extend the class BasicImportHelper()
#
# That means you just have to overload the methods you want to
# change, leaving the other ones inteact.
#
# Something that you might want to do is use transactions, for example.
#
# Also, don't forget to add the necessary Django imports.
#
# This file was generated with the following command:
# ./manage.py dumpscript strategy
#
# to restore it, run
# manage.py runscript module_name.this_script_name
#
# example: if manage.py is at ./manage.py
# and the script is at ./some_folder/some_script.py
# you must make sure ./some_folder/__init__.py exists
# and run  ./manage.py runscript some_folder.some_script
import os, sys
from django.db import transaction

class BasicImportHelper(object):

    def pre_import(self):
        pass

    @transaction.atomic
    def run_import(self, import_data):
        import_data()

    def post_import(self):
        pass

    def locate_similar(self, current_object, search_data):
        # You will probably want to call this method from save_or_locate()
        # Example:
        #   new_obj = self.locate_similar(the_obj, {"national_id": the_obj.national_id } )

        the_obj = current_object.__class__.objects.get(**search_data)
        return the_obj

    def locate_object(self, original_class, original_pk_name, the_class, pk_name, pk_value, obj_content):
        # You may change this function to do specific lookup for specific objects
        #
        # original_class class of the django orm's object that needs to be located
        # original_pk_name the primary key of original_class
        # the_class      parent class of original_class which contains obj_content
        # pk_name        the primary key of original_class
        # pk_value       value of the primary_key
        # obj_content    content of the object which was not exported.
        #
        # You should use obj_content to locate the object on the target db
        #
        # An example where original_class and the_class are different is
        # when original_class is Farmer and the_class is Person. The table
        # may refer to a Farmer but you will actually need to locate Person
        # in order to instantiate that Farmer
        #
        # Example:
        #   if the_class == SurveyResultFormat or the_class == SurveyType or the_class == SurveyState:
        #       pk_name="name"
        #       pk_value=obj_content[pk_name]
        #   if the_class == StaffGroup:
        #       pk_value=8

        search_data = { pk_name: pk_value }
        the_obj = the_class.objects.get(**search_data)
        #print(the_obj)
        return the_obj


    def save_or_locate(self, the_obj):
        # Change this if you want to locate the object in the database
        try:
            the_obj.save()
        except:
            print("---------------")
            print("Error saving the following object:")
            print(the_obj.__class__)
            print(" ")
            print(the_obj.__dict__)
            print(" ")
            print(the_obj)
            print(" ")
            print("---------------")

            raise
        return the_obj


importer = None
try:
    import import_helper
    # We need this so ImportHelper can extend BasicImportHelper, although import_helper.py
    # has no knowlodge of this class
    importer = type("DynamicImportHelper", (import_helper.ImportHelper, BasicImportHelper ) , {} )()
except ImportError as e:
    # From Python 3.3 we can check e.name - string match is for backward compatibility.
    if 'import_helper' in str(e):
        importer = BasicImportHelper()
    else:
        raise

import datetime
from decimal import Decimal
from django.contrib.contenttypes.models import ContentType

try:
    import dateutil.parser
except ImportError:
    print("Please install python-dateutil")
    sys.exit(os.EX_USAGE)

def run():
    importer.pre_import()
    importer.run_import(import_data)
    importer.post_import()

def import_data():
    # Initial Imports
    from customers.models import Customer

    # Processing model: strategy.models.StrategicTheme

    from strategy.models import StrategicTheme

    strategy_strategictheme_1 = StrategicTheme()
    strategy_strategictheme_1.created = dateutil.parser.parse("2017-04-12T06:16:53.483953+00:00")
    strategy_strategictheme_1.modified = dateutil.parser.parse("2017-04-12T06:16:53.484020+00:00")
    strategy_strategictheme_1.name = 'Customer Delight'
    strategy_strategictheme_1.description = ''
    strategy_strategictheme_1.customer = Customer.objects.first()
    strategy_strategictheme_1.active = True
    strategy_strategictheme_1 = importer.save_or_locate(strategy_strategictheme_1)

    strategy_strategictheme_2 = StrategicTheme()
    strategy_strategictheme_2.created = dateutil.parser.parse("2017-03-31T13:28:19.514703+00:00")
    strategy_strategictheme_2.modified = dateutil.parser.parse("2017-03-31T13:28:19.514759+00:00")
    strategy_strategictheme_2.name = 'Massive Profits'
    strategy_strategictheme_2.description = ''
    strategy_strategictheme_2.customer = Customer.objects.first()
    strategy_strategictheme_2.active = True
    strategy_strategictheme_2 = importer.save_or_locate(strategy_strategictheme_2)

    strategy_strategictheme_3 = StrategicTheme()
    strategy_strategictheme_3.created = dateutil.parser.parse("2017-04-12T06:18:49.652026+00:00")
    strategy_strategictheme_3.modified = dateutil.parser.parse("2017-04-12T06:18:49.652086+00:00")
    strategy_strategictheme_3.name = 'Product Leadership'
    strategy_strategictheme_3.description = ''
    strategy_strategictheme_3.customer = Customer.objects.first()
    strategy_strategictheme_3.active = True
    strategy_strategictheme_3 = importer.save_or_locate(strategy_strategictheme_3)

    # Processing model: strategy.models.Objective

    from strategy.models import Objective

    strategy_objective_1 = Objective()
    strategy_objective_1.created = dateutil.parser.parse("2017-04-12T06:10:44.121788+00:00")
    strategy_objective_1.modified = dateutil.parser.parse("2017-04-12T06:10:44.121911+00:00")
    strategy_objective_1.name = 'Decrease Operating Costs'
    strategy_objective_1.description = ''
    strategy_objective_1.strategic_theme = strategy_strategictheme_2
    strategy_objective_1.parent = None
    strategy_objective_1.customer = Customer.objects.first()
    strategy_objective_1.active = True
    strategy_objective_1.lft = 1
    strategy_objective_1.rght = 2
    strategy_objective_1.tree_id = 1
    strategy_objective_1.level = 0
    strategy_objective_1 = importer.save_or_locate(strategy_objective_1)

    strategy_objective_2 = Objective()
    strategy_objective_2.created = dateutil.parser.parse("2017-04-12T06:17:18.415746+00:00")
    strategy_objective_2.modified = dateutil.parser.parse("2017-04-12T06:17:18.415804+00:00")
    strategy_objective_2.name = 'Improve End User Experience'
    strategy_objective_2.description = ''
    strategy_objective_2.strategic_theme = strategy_strategictheme_1
    strategy_objective_2.parent = None
    strategy_objective_2.customer = Customer.objects.first()
    strategy_objective_2.active = True
    strategy_objective_2.lft = 1
    strategy_objective_2.rght = 2
    strategy_objective_2.tree_id = 2
    strategy_objective_2.level = 0
    strategy_objective_2 = importer.save_or_locate(strategy_objective_2)

    strategy_objective_3 = Objective()
    strategy_objective_3.created = dateutil.parser.parse("2017-04-12T06:18:06.140250+00:00")
    strategy_objective_3.modified = dateutil.parser.parse("2017-04-12T06:18:06.140472+00:00")
    strategy_objective_3.name = 'Improve offering selection'
    strategy_objective_3.description = ''
    strategy_objective_3.strategic_theme = strategy_strategictheme_1
    strategy_objective_3.parent = None
    strategy_objective_3.customer = Customer.objects.first()
    strategy_objective_3.active = True
    strategy_objective_3.lft = 1
    strategy_objective_3.rght = 2
    strategy_objective_3.tree_id = 3
    strategy_objective_3.level = 0
    strategy_objective_3 = importer.save_or_locate(strategy_objective_3)

    strategy_objective_4 = Objective()
    strategy_objective_4.created = dateutil.parser.parse("2017-04-12T06:19:29.347814+00:00")
    strategy_objective_4.modified = dateutil.parser.parse("2017-04-12T06:19:29.347905+00:00")
    strategy_objective_4.name = 'Improve technology'
    strategy_objective_4.description = ''
    strategy_objective_4.strategic_theme = strategy_strategictheme_3
    strategy_objective_4.parent = None
    strategy_objective_4.customer = Customer.objects.first()
    strategy_objective_4.active = True
    strategy_objective_4.lft = 1
    strategy_objective_4.rght = 2
    strategy_objective_4.tree_id = 4
    strategy_objective_4.level = 0
    strategy_objective_4 = importer.save_or_locate(strategy_objective_4)

    strategy_objective_5 = Objective()
    strategy_objective_5.created = dateutil.parser.parse("2017-03-31T13:28:27.242602+00:00")
    strategy_objective_5.modified = dateutil.parser.parse("2017-03-31T13:28:27.242681+00:00")
    strategy_objective_5.name = 'Increase Profit'
    strategy_objective_5.description = ''
    strategy_objective_5.strategic_theme = strategy_strategictheme_2
    strategy_objective_5.parent = None
    strategy_objective_5.customer = Customer.objects.first()
    strategy_objective_5.active = True
    strategy_objective_5.lft = 1
    strategy_objective_5.rght = 2
    strategy_objective_5.tree_id = 5
    strategy_objective_5.level = 0
    strategy_objective_5 = importer.save_or_locate(strategy_objective_5)

    strategy_objective_6 = Objective()
    strategy_objective_6.created = dateutil.parser.parse("2017-04-12T06:09:50.247608+00:00")
    strategy_objective_6.modified = dateutil.parser.parse("2017-04-12T06:09:50.247696+00:00")
    strategy_objective_6.name = 'Increase Revenue'
    strategy_objective_6.description = ''
    strategy_objective_6.strategic_theme = strategy_strategictheme_2
    strategy_objective_6.parent = None
    strategy_objective_6.customer = Customer.objects.first()
    strategy_objective_6.active = True
    strategy_objective_6.lft = 1
    strategy_objective_6.rght = 2
    strategy_objective_6.tree_id = 6
    strategy_objective_6.level = 0
    strategy_objective_6 = importer.save_or_locate(strategy_objective_6)

