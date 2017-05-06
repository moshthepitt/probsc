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
# ./manage.py dumpscript kpis
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
    from strategy.models import Objective

    # Processing model: kpis.models.KPI

    from kpis.models import KPI

    kpis_kpi_1 = KPI()
    kpis_kpi_1.created = dateutil.parser.parse("2017-03-31T13:31:39.721746+00:00")
    kpis_kpi_1.modified = dateutil.parser.parse("2017-04-11T14:27:17.340798+00:00")
    kpis_kpi_1.objective =  importer.locate_object(Objective, "id", Objective, "id", 1, {'_mptt_cached_fields': "{'name': 'Increase Profit', 'parent': None}", 'created': datetime.datetime(2017, 3, 31, 13, 28, 27, 242602, tzinfo=<UTC>), 'level': 0, 'rght': 2, 'name': 'Increase Profit', 'id': 1, 'customer_id': 1, 'parent_id': None, 'description': '', 'active': True, 'tree_id': 5, 'lft': 1, 'modified': datetime.datetime(2017, 3, 31, 13, 28, 27, 242681, tzinfo=<UTC>), 'strategic_theme_id': 1} ) 
    kpis_kpi_1.name = 'Descrease costs'
    kpis_kpi_1.measure = 'Operating costs'
    kpis_kpi_1.description = ''
    kpis_kpi_1.perspective = '1'
    kpis_kpi_1.baseline = Decimal('250.00')
    kpis_kpi_1.target = Decimal('150.00')
    kpis_kpi_1.unit = '1'
    kpis_kpi_1.direction = '2'
    kpis_kpi_1.weight = Decimal('20.00')
    kpis_kpi_1.reporting_period = '4'
    kpis_kpi_1.calculation = '1'
    kpis_kpi_1.reporting_method = '1'
    kpis_kpi_1.customer =  importer.locate_object(Customer, "id", Customer, "id", 1, {'financial_year_end_month': 12, 'created': datetime.datetime(2017, 3, 31, 13, 27, 37, 470821, tzinfo=<UTC>), 'email': '', 'financial_year_end_day': 31, 'id': 1, 'description': '', 'name': 'Nickel Pro', 'active': True, 'review_rounds': 2, 'modified': datetime.datetime(2017, 3, 31, 13, 27, 37, 470881, tzinfo=<UTC>), 'phone': ''} ) 
    kpis_kpi_1.active = True
    kpis_kpi_1 = importer.save_or_locate(kpis_kpi_1)

    kpis_kpi_2 = KPI()
    kpis_kpi_2.created = dateutil.parser.parse("2017-03-31T13:29:22.462839+00:00")
    kpis_kpi_2.modified = dateutil.parser.parse("2017-03-31T13:29:22.462899+00:00")
    kpis_kpi_2.objective =  importer.locate_object(Objective, "id", Objective, "id", 1, {'_mptt_cached_fields': "{'name': 'Increase Profit', 'parent': None}", 'created': datetime.datetime(2017, 3, 31, 13, 28, 27, 242602, tzinfo=<UTC>), 'level': 0, 'rght': 2, 'name': 'Increase Profit', 'id': 1, 'customer_id': 1, 'parent_id': None, 'description': '', 'active': True, 'tree_id': 5, 'lft': 1, 'modified': datetime.datetime(2017, 3, 31, 13, 28, 27, 242681, tzinfo=<UTC>), 'strategic_theme_id': 1} ) 
    kpis_kpi_2.name = 'Increase Revenue'
    kpis_kpi_2.measure = 'Sales'
    kpis_kpi_2.description = ''
    kpis_kpi_2.perspective = '1'
    kpis_kpi_2.baseline = Decimal('1000.00')
    kpis_kpi_2.target = Decimal('2300.00')
    kpis_kpi_2.unit = '1'
    kpis_kpi_2.direction = '1'
    kpis_kpi_2.weight = Decimal('60.00')
    kpis_kpi_2.reporting_period = '5'
    kpis_kpi_2.calculation = '1'
    kpis_kpi_2.reporting_method = '1'
    kpis_kpi_2.customer =  importer.locate_object(Customer, "id", Customer, "id", 1, {'financial_year_end_month': 12, 'created': datetime.datetime(2017, 3, 31, 13, 27, 37, 470821, tzinfo=<UTC>), 'email': '', 'financial_year_end_day': 31, 'id': 1, 'description': '', 'name': 'Nickel Pro', 'active': True, 'review_rounds': 2, 'modified': datetime.datetime(2017, 3, 31, 13, 27, 37, 470881, tzinfo=<UTC>), 'phone': ''} ) 
    kpis_kpi_2.active = True
    kpis_kpi_2 = importer.save_or_locate(kpis_kpi_2)

    kpis_kpi_3 = KPI()
    kpis_kpi_3.created = dateutil.parser.parse("2017-04-12T06:30:16.112211+00:00")
    kpis_kpi_3.modified = dateutil.parser.parse("2017-04-12T06:30:16.112272+00:00")
    kpis_kpi_3.objective =  importer.locate_object(Objective, "id", Objective, "id", 1, {'_mptt_cached_fields': "{'name': 'Increase Profit', 'parent': None}", 'created': datetime.datetime(2017, 3, 31, 13, 28, 27, 242602, tzinfo=<UTC>), 'level': 0, 'rght': 2, 'name': 'Increase Profit', 'id': 1, 'customer_id': 1, 'parent_id': None, 'description': '', 'active': True, 'tree_id': 5, 'lft': 1, 'modified': datetime.datetime(2017, 3, 31, 13, 28, 27, 242681, tzinfo=<UTC>), 'strategic_theme_id': 1} ) 
    kpis_kpi_3.name = 'Increase net profit'
    kpis_kpi_3.measure = 'Net profit'
    kpis_kpi_3.description = ''
    kpis_kpi_3.perspective = '1'
    kpis_kpi_3.baseline = Decimal('0.00')
    kpis_kpi_3.target = Decimal('5.00')
    kpis_kpi_3.unit = '3'
    kpis_kpi_3.direction = '1'
    kpis_kpi_3.weight = Decimal('10.00')
    kpis_kpi_3.reporting_period = '3'
    kpis_kpi_3.calculation = '2'
    kpis_kpi_3.reporting_method = '1'
    kpis_kpi_3.customer =  importer.locate_object(Customer, "id", Customer, "id", 1, {'financial_year_end_month': 12, 'created': datetime.datetime(2017, 3, 31, 13, 27, 37, 470821, tzinfo=<UTC>), 'email': '', 'financial_year_end_day': 31, 'id': 1, 'description': '', 'name': 'Nickel Pro', 'active': True, 'review_rounds': 2, 'modified': datetime.datetime(2017, 3, 31, 13, 27, 37, 470881, tzinfo=<UTC>), 'phone': ''} ) 
    kpis_kpi_3.active = True
    kpis_kpi_3 = importer.save_or_locate(kpis_kpi_3)

    kpis_kpi_4 = KPI()
    kpis_kpi_4.created = dateutil.parser.parse("2017-03-31T13:30:45.516806+00:00")
    kpis_kpi_4.modified = dateutil.parser.parse("2017-03-31T13:30:45.516904+00:00")
    kpis_kpi_4.objective =  importer.locate_object(Objective, "id", Objective, "id", 1, {'_mptt_cached_fields': "{'name': 'Increase Profit', 'parent': None}", 'created': datetime.datetime(2017, 3, 31, 13, 28, 27, 242602, tzinfo=<UTC>), 'level': 0, 'rght': 2, 'name': 'Increase Profit', 'id': 1, 'customer_id': 1, 'parent_id': None, 'description': '', 'active': True, 'tree_id': 5, 'lft': 1, 'modified': datetime.datetime(2017, 3, 31, 13, 28, 27, 242681, tzinfo=<UTC>), 'strategic_theme_id': 1} ) 
    kpis_kpi_4.name = 'Maintain salaries'
    kpis_kpi_4.measure = 'Total payroll'
    kpis_kpi_4.description = ''
    kpis_kpi_4.perspective = '1'
    kpis_kpi_4.baseline = Decimal('1000000.00')
    kpis_kpi_4.target = Decimal('1000000.00')
    kpis_kpi_4.unit = '1'
    kpis_kpi_4.direction = '1'
    kpis_kpi_4.weight = Decimal('20.00')
    kpis_kpi_4.reporting_period = '5'
    kpis_kpi_4.calculation = '2'
    kpis_kpi_4.reporting_method = '1'
    kpis_kpi_4.customer =  importer.locate_object(Customer, "id", Customer, "id", 1, {'financial_year_end_month': 12, 'created': datetime.datetime(2017, 3, 31, 13, 27, 37, 470821, tzinfo=<UTC>), 'email': '', 'financial_year_end_day': 31, 'id': 1, 'description': '', 'name': 'Nickel Pro', 'active': True, 'review_rounds': 2, 'modified': datetime.datetime(2017, 3, 31, 13, 27, 37, 470881, tzinfo=<UTC>), 'phone': ''} ) 
    kpis_kpi_4.active = True
    kpis_kpi_4 = importer.save_or_locate(kpis_kpi_4)

    kpis_kpi_5 = KPI()
    kpis_kpi_5.created = dateutil.parser.parse("2017-04-12T06:31:08.547417+00:00")
    kpis_kpi_5.modified = dateutil.parser.parse("2017-04-12T06:43:12.330551+00:00")
    kpis_kpi_5.objective =  importer.locate_object(Objective, "id", Objective, "id", 5, {'_mptt_cached_fields': "{'name': 'Decrease Operating Costs', 'parent': None}", 'created': datetime.datetime(2017, 4, 12, 6, 10, 44, 121788, tzinfo=<UTC>), 'level': 0, 'rght': 2, 'name': 'Decrease Operating Costs', 'id': 5, 'customer_id': 1, 'parent_id': None, 'description': '', 'active': True, 'tree_id': 1, 'lft': 1, 'modified': datetime.datetime(2017, 4, 12, 6, 10, 44, 121911, tzinfo=<UTC>), 'strategic_theme_id': 1} ) 
    kpis_kpi_5.name = 'Reduce operating costs'
    kpis_kpi_5.measure = 'Operating costs'
    kpis_kpi_5.description = ''
    kpis_kpi_5.perspective = '1'
    kpis_kpi_5.baseline = Decimal('0.00')
    kpis_kpi_5.target = Decimal('12000000.00')
    kpis_kpi_5.unit = '1'
    kpis_kpi_5.direction = '2'
    kpis_kpi_5.weight = Decimal('10.00')
    kpis_kpi_5.reporting_period = '5'
    kpis_kpi_5.calculation = '1'
    kpis_kpi_5.reporting_method = '1'
    kpis_kpi_5.customer =  importer.locate_object(Customer, "id", Customer, "id", 1, {'financial_year_end_month': 12, 'created': datetime.datetime(2017, 3, 31, 13, 27, 37, 470821, tzinfo=<UTC>), 'email': '', 'financial_year_end_day': 31, 'id': 1, 'description': '', 'name': 'Nickel Pro', 'active': True, 'review_rounds': 2, 'modified': datetime.datetime(2017, 3, 31, 13, 27, 37, 470881, tzinfo=<UTC>), 'phone': ''} ) 
    kpis_kpi_5.active = True
    kpis_kpi_5 = importer.save_or_locate(kpis_kpi_5)

    kpis_kpi_6 = KPI()
    kpis_kpi_6.created = dateutil.parser.parse("2017-04-12T06:32:14.328666+00:00")
    kpis_kpi_6.modified = dateutil.parser.parse("2017-04-12T06:32:14.328748+00:00")
    kpis_kpi_6.objective =  importer.locate_object(Objective, "id", Objective, "id", 6, {'_mptt_cached_fields': "{'name': 'Improve End User Experience', 'parent': None}", 'created': datetime.datetime(2017, 4, 12, 6, 17, 18, 415746, tzinfo=<UTC>), 'level': 0, 'rght': 2, 'name': 'Improve End User Experience', 'id': 6, 'customer_id': 1, 'parent_id': None, 'description': '', 'active': True, 'tree_id': 2, 'lft': 1, 'modified': datetime.datetime(2017, 4, 12, 6, 17, 18, 415804, tzinfo=<UTC>), 'strategic_theme_id': 9} ) 
    kpis_kpi_6.name = 'Customer satisfaction'
    kpis_kpi_6.measure = 'Customer satisfaction index'
    kpis_kpi_6.description = ''
    kpis_kpi_6.perspective = '2'
    kpis_kpi_6.baseline = Decimal('0.00')
    kpis_kpi_6.target = Decimal('80.00')
    kpis_kpi_6.unit = '3'
    kpis_kpi_6.direction = '1'
    kpis_kpi_6.weight = Decimal('10.00')
    kpis_kpi_6.reporting_period = '4'
    kpis_kpi_6.calculation = '2'
    kpis_kpi_6.reporting_method = '1'
    kpis_kpi_6.customer =  importer.locate_object(Customer, "id", Customer, "id", 1, {'financial_year_end_month': 12, 'created': datetime.datetime(2017, 3, 31, 13, 27, 37, 470821, tzinfo=<UTC>), 'email': '', 'financial_year_end_day': 31, 'id': 1, 'description': '', 'name': 'Nickel Pro', 'active': True, 'review_rounds': 2, 'modified': datetime.datetime(2017, 3, 31, 13, 27, 37, 470881, tzinfo=<UTC>), 'phone': ''} ) 
    kpis_kpi_6.active = True
    kpis_kpi_6 = importer.save_or_locate(kpis_kpi_6)

    kpis_kpi_7 = KPI()
    kpis_kpi_7.created = dateutil.parser.parse("2017-04-09T09:12:19.851575+00:00")
    kpis_kpi_7.modified = dateutil.parser.parse("2017-04-09T09:12:19.851663+00:00")
    kpis_kpi_7.objective =  importer.locate_object(Objective, "id", Objective, "id", 1, {'_mptt_cached_fields': "{'name': 'Increase Profit', 'parent': None}", 'created': datetime.datetime(2017, 3, 31, 13, 28, 27, 242602, tzinfo=<UTC>), 'level': 0, 'rght': 2, 'name': 'Increase Profit', 'id': 1, 'customer_id': 1, 'parent_id': None, 'description': '', 'active': True, 'tree_id': 5, 'lft': 1, 'modified': datetime.datetime(2017, 3, 31, 13, 28, 27, 242681, tzinfo=<UTC>), 'strategic_theme_id': 1} ) 
    kpis_kpi_7.name = 'Improve external customer satisfaction'
    kpis_kpi_7.measure = 'Customer satisfaction index'
    kpis_kpi_7.description = 'Accrued leave days at end year'
    kpis_kpi_7.perspective = '2'
    kpis_kpi_7.baseline = Decimal('60.00')
    kpis_kpi_7.target = Decimal('80.00')
    kpis_kpi_7.unit = '3'
    kpis_kpi_7.direction = '1'
    kpis_kpi_7.weight = Decimal('9.00')
    kpis_kpi_7.reporting_period = '5'
    kpis_kpi_7.calculation = '1'
    kpis_kpi_7.reporting_method = '1'
    kpis_kpi_7.customer =  importer.locate_object(Customer, "id", Customer, "id", 1, {'financial_year_end_month': 12, 'created': datetime.datetime(2017, 3, 31, 13, 27, 37, 470821, tzinfo=<UTC>), 'email': '', 'financial_year_end_day': 31, 'id': 1, 'description': '', 'name': 'Nickel Pro', 'active': True, 'review_rounds': 2, 'modified': datetime.datetime(2017, 3, 31, 13, 27, 37, 470881, tzinfo=<UTC>), 'phone': ''} ) 
    kpis_kpi_7.active = True
    kpis_kpi_7 = importer.save_or_locate(kpis_kpi_7)

    kpis_kpi_8 = KPI()
    kpis_kpi_8.created = dateutil.parser.parse("2017-04-12T06:33:50.309875+00:00")
    kpis_kpi_8.modified = dateutil.parser.parse("2017-04-12T06:44:34.865653+00:00")
    kpis_kpi_8.objective =  importer.locate_object(Objective, "id", Objective, "id", 6, {'_mptt_cached_fields': "{'name': 'Improve End User Experience', 'parent': None}", 'created': datetime.datetime(2017, 4, 12, 6, 17, 18, 415746, tzinfo=<UTC>), 'level': 0, 'rght': 2, 'name': 'Improve End User Experience', 'id': 6, 'customer_id': 1, 'parent_id': None, 'description': '', 'active': True, 'tree_id': 2, 'lft': 1, 'modified': datetime.datetime(2017, 4, 12, 6, 17, 18, 415804, tzinfo=<UTC>), 'strategic_theme_id': 9} ) 
    kpis_kpi_8.name = 'Market share'
    kpis_kpi_8.measure = 'Market share index'
    kpis_kpi_8.description = ''
    kpis_kpi_8.perspective = '2'
    kpis_kpi_8.baseline = Decimal('0.00')
    kpis_kpi_8.target = Decimal('30.00')
    kpis_kpi_8.unit = '3'
    kpis_kpi_8.direction = '1'
    kpis_kpi_8.weight = Decimal('10.00')
    kpis_kpi_8.reporting_period = '5'
    kpis_kpi_8.calculation = '1'
    kpis_kpi_8.reporting_method = '1'
    kpis_kpi_8.customer =  importer.locate_object(Customer, "id", Customer, "id", 1, {'financial_year_end_month': 12, 'created': datetime.datetime(2017, 3, 31, 13, 27, 37, 470821, tzinfo=<UTC>), 'email': '', 'financial_year_end_day': 31, 'id': 1, 'description': '', 'name': 'Nickel Pro', 'active': True, 'review_rounds': 2, 'modified': datetime.datetime(2017, 3, 31, 13, 27, 37, 470881, tzinfo=<UTC>), 'phone': ''} ) 
    kpis_kpi_8.active = True
    kpis_kpi_8 = importer.save_or_locate(kpis_kpi_8)

    kpis_kpi_9 = KPI()
    kpis_kpi_9.created = dateutil.parser.parse("2017-04-11T13:47:43.001071+00:00")
    kpis_kpi_9.modified = dateutil.parser.parse("2017-04-11T13:47:43.001156+00:00")
    kpis_kpi_9.objective =  importer.locate_object(Objective, "id", Objective, "id", 1, {'_mptt_cached_fields': "{'name': 'Increase Profit', 'parent': None}", 'created': datetime.datetime(2017, 3, 31, 13, 28, 27, 242602, tzinfo=<UTC>), 'level': 0, 'rght': 2, 'name': 'Increase Profit', 'id': 1, 'customer_id': 1, 'parent_id': None, 'description': '', 'active': True, 'tree_id': 5, 'lft': 1, 'modified': datetime.datetime(2017, 3, 31, 13, 28, 27, 242681, tzinfo=<UTC>), 'strategic_theme_id': 1} ) 
    kpis_kpi_9.name = 'Another'
    kpis_kpi_9.measure = 'Another'
    kpis_kpi_9.description = ''
    kpis_kpi_9.perspective = '3'
    kpis_kpi_9.baseline = Decimal('100.00')
    kpis_kpi_9.target = Decimal('150.00')
    kpis_kpi_9.unit = '2'
    kpis_kpi_9.direction = '1'
    kpis_kpi_9.weight = Decimal('23.00')
    kpis_kpi_9.reporting_period = '5'
    kpis_kpi_9.calculation = '1'
    kpis_kpi_9.reporting_method = '1'
    kpis_kpi_9.customer =  importer.locate_object(Customer, "id", Customer, "id", 1, {'financial_year_end_month': 12, 'created': datetime.datetime(2017, 3, 31, 13, 27, 37, 470821, tzinfo=<UTC>), 'email': '', 'financial_year_end_day': 31, 'id': 1, 'description': '', 'name': 'Nickel Pro', 'active': True, 'review_rounds': 2, 'modified': datetime.datetime(2017, 3, 31, 13, 27, 37, 470881, tzinfo=<UTC>), 'phone': ''} ) 
    kpis_kpi_9.active = True
    kpis_kpi_9 = importer.save_or_locate(kpis_kpi_9)

    kpis_kpi_10 = KPI()
    kpis_kpi_10.created = dateutil.parser.parse("2017-04-12T06:35:23.839035+00:00")
    kpis_kpi_10.modified = dateutil.parser.parse("2017-04-12T06:35:23.839125+00:00")
    kpis_kpi_10.objective =  importer.locate_object(Objective, "id", Objective, "id", 7, {'_mptt_cached_fields': "{'name': 'Improve offering selection', 'parent': None}", 'created': datetime.datetime(2017, 4, 12, 6, 18, 6, 140250, tzinfo=<UTC>), 'level': 0, 'rght': 2, 'name': 'Improve offering selection', 'id': 7, 'customer_id': 1, 'parent_id': None, 'description': '', 'active': True, 'tree_id': 3, 'lft': 1, 'modified': datetime.datetime(2017, 4, 12, 6, 18, 6, 140472, tzinfo=<UTC>), 'strategic_theme_id': 9} ) 
    kpis_kpi_10.name = 'New products'
    kpis_kpi_10.measure = 'New products as a % of sales'
    kpis_kpi_10.description = ''
    kpis_kpi_10.perspective = '3'
    kpis_kpi_10.baseline = Decimal('0.00')
    kpis_kpi_10.target = Decimal('10.00')
    kpis_kpi_10.unit = '3'
    kpis_kpi_10.direction = '1'
    kpis_kpi_10.weight = Decimal('10.00')
    kpis_kpi_10.reporting_period = '5'
    kpis_kpi_10.calculation = '1'
    kpis_kpi_10.reporting_method = '1'
    kpis_kpi_10.customer =  importer.locate_object(Customer, "id", Customer, "id", 1, {'financial_year_end_month': 12, 'created': datetime.datetime(2017, 3, 31, 13, 27, 37, 470821, tzinfo=<UTC>), 'email': '', 'financial_year_end_day': 31, 'id': 1, 'description': '', 'name': 'Nickel Pro', 'active': True, 'review_rounds': 2, 'modified': datetime.datetime(2017, 3, 31, 13, 27, 37, 470881, tzinfo=<UTC>), 'phone': ''} ) 
    kpis_kpi_10.active = True
    kpis_kpi_10 = importer.save_or_locate(kpis_kpi_10)

    kpis_kpi_11 = KPI()
    kpis_kpi_11.created = dateutil.parser.parse("2017-04-12T06:42:54.109498+00:00")
    kpis_kpi_11.modified = dateutil.parser.parse("2017-04-12T06:42:54.109600+00:00")
    kpis_kpi_11.objective =  importer.locate_object(Objective, "id", Objective, "id", 8, {'_mptt_cached_fields': "{'name': 'Improve technology', 'parent': None}", 'created': datetime.datetime(2017, 4, 12, 6, 19, 29, 347814, tzinfo=<UTC>), 'level': 0, 'rght': 2, 'name': 'Improve technology', 'id': 8, 'customer_id': 1, 'parent_id': None, 'description': '', 'active': True, 'tree_id': 4, 'lft': 1, 'modified': datetime.datetime(2017, 4, 12, 6, 19, 29, 347905, tzinfo=<UTC>), 'strategic_theme_id': 10} ) 
    kpis_kpi_11.name = 'Adoption of new technologies'
    kpis_kpi_11.measure = 'Technology training index'
    kpis_kpi_11.description = ''
    kpis_kpi_11.perspective = '4'
    kpis_kpi_11.baseline = Decimal('0.00')
    kpis_kpi_11.target = Decimal('70.00')
    kpis_kpi_11.unit = '3'
    kpis_kpi_11.direction = '1'
    kpis_kpi_11.weight = Decimal('10.00')
    kpis_kpi_11.reporting_period = '5'
    kpis_kpi_11.calculation = '1'
    kpis_kpi_11.reporting_method = '1'
    kpis_kpi_11.customer =  importer.locate_object(Customer, "id", Customer, "id", 1, {'financial_year_end_month': 12, 'created': datetime.datetime(2017, 3, 31, 13, 27, 37, 470821, tzinfo=<UTC>), 'email': '', 'financial_year_end_day': 31, 'id': 1, 'description': '', 'name': 'Nickel Pro', 'active': True, 'review_rounds': 2, 'modified': datetime.datetime(2017, 3, 31, 13, 27, 37, 470881, tzinfo=<UTC>), 'phone': ''} ) 
    kpis_kpi_11.active = True
    kpis_kpi_11 = importer.save_or_locate(kpis_kpi_11)

