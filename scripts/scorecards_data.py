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
# ./manage.py dumpscript scorecards
#
# to restore it, run
# manage.py runscript module_name.this_script_name
#
# example: if manage.py is at ./manage.py
# and the script is at ./some_folder/some_script.py
# you must make sure ./some_folder/__init__.py exists
# and run  ./manage.py runscript some_folder.some_script
import os
import sys
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
        #   new_obj = self.locate_similar(the_obj, {"national_id": the_obj.national_id})

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

        search_data = {pk_name: pk_value}
        the_obj = the_class.objects.get(**search_data)
        # print(the_obj)
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
    importer = type("DynamicImportHelper", (import_helper.ImportHelper, BasicImportHelper), {})()
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
    from django.contrib.auth.models import User
    from customers.models import Customer
    from kpis.models import KPI

    # Processing model: scorecards.models.Scorecard

    from scorecards.models import Scorecard

    scorecards_scorecard_1 = Scorecard()
    scorecards_scorecard_1.created = dateutil.parser.parse("2017-03-31T13:33:38.127237+00:00")
    scorecards_scorecard_1.modified = dateutil.parser.parse("2017-04-11T07:36:39.950136+00:00")
    scorecards_scorecard_1.name = 'Generic'
    scorecards_scorecard_1.year = 2017
    scorecards_scorecard_1.description = ''
    scorecards_scorecard_1.user = User.objects.first()
    scorecards_scorecard_1.customer = Customer.objects.first()
    scorecards_scorecard_1.active = True
    scorecards_scorecard_1 = importer.save_or_locate(scorecards_scorecard_1)

    scorecards_scorecard_2 = Scorecard()
    scorecards_scorecard_2.created = dateutil.parser.parse("2017-04-12T06:28:46.722604+00:00")
    scorecards_scorecard_2.modified = dateutil.parser.parse("2017-04-12T06:28:46.722665+00:00")
    scorecards_scorecard_2.name = 'Test'
    scorecards_scorecard_2.year = 2017
    scorecards_scorecard_2.description = ''
    scorecards_scorecard_2.user = User.objects.first()
    scorecards_scorecard_2.customer = Customer.objects.first()
    scorecards_scorecard_2.active = True
    scorecards_scorecard_2 = importer.save_or_locate(scorecards_scorecard_2)

    # Processing model: scorecards.models.Evidence

    # from scorecards.models import Evidence

    # Processing model: scorecards.models.Score

    from scorecards.models import Score

    scorecards_score_1 = Score()
    scorecards_score_1.created = dateutil.parser.parse("2017-03-31T13:35:49.528772+00:00")
    scorecards_score_1.modified = dateutil.parser.parse("2017-03-31T13:35:49.528844+00:00")
    scorecards_score_1.date = dateutil.parser.parse("2017-03-31")
    scorecards_score_1.scorecard = scorecards_scorecard_1
    scorecards_score_1.kpi = importer.locate_object(KPI, "id", KPI, "id", 1, {})
    scorecards_score_1.value = Decimal('2345.00')
    scorecards_score_1.review_round = 1
    scorecards_score_1.notes = ''
    scorecards_score_1 = importer.save_or_locate(scorecards_score_1)

    scorecards_score_2 = Score()
    scorecards_score_2.created = dateutil.parser.parse("2017-03-31T13:36:21.369835+00:00")
    scorecards_score_2.modified = dateutil.parser.parse("2017-03-31T13:36:21.369920+00:00")
    scorecards_score_2.date = dateutil.parser.parse("2017-03-31")
    scorecards_score_2.scorecard = scorecards_scorecard_1
    scorecards_score_2.kpi = importer.locate_object(KPI, "id", KPI, "id", 2, {})
    scorecards_score_2.value = Decimal('1000100.00')
    scorecards_score_2.review_round = 1
    scorecards_score_2.notes = ''
    scorecards_score_2 = importer.save_or_locate(scorecards_score_2)

    scorecards_score_3 = Score()
    scorecards_score_3.created = dateutil.parser.parse("2017-03-31T13:38:32.815904+00:00")
    scorecards_score_3.modified = dateutil.parser.parse("2017-03-31T13:38:32.815964+00:00")
    scorecards_score_3.date = dateutil.parser.parse("2017-03-31")
    scorecards_score_3.scorecard = scorecards_scorecard_1
    scorecards_score_3.kpi = importer.locate_object(KPI, "id", KPI, "id", 3, {})
    scorecards_score_3.value = Decimal('75.00')
    scorecards_score_3.review_round = 1
    scorecards_score_3.notes = ''
    scorecards_score_3 = importer.save_or_locate(scorecards_score_3)

    scorecards_score_4 = Score()
    scorecards_score_4.created = dateutil.parser.parse("2017-03-31T13:38:41.902709+00:00")
    scorecards_score_4.modified = dateutil.parser.parse("2017-03-31T13:38:41.902789+00:00")
    scorecards_score_4.date = dateutil.parser.parse("2017-03-31")
    scorecards_score_4.scorecard = scorecards_scorecard_1
    scorecards_score_4.kpi = importer.locate_object(KPI, "id", KPI, "id", 3, {})
    scorecards_score_4.value = Decimal('80.00')
    scorecards_score_4.review_round = 1
    scorecards_score_4.notes = ''
    scorecards_score_4 = importer.save_or_locate(scorecards_score_4)

    # Processing model: scorecards.models.ScorecardKPI

    from scorecards.models import ScorecardKPI

    scorecards_scorecardkpi_1 = ScorecardKPI()
    scorecards_scorecardkpi_1.created = dateutil.parser.parse("2017-03-31T13:34:27.969131+00:00")
    scorecards_scorecardkpi_1.modified = dateutil.parser.parse("2017-04-08T11:07:52.118435+00:00")
    scorecards_scorecardkpi_1.scorecard = scorecards_scorecard_1
    scorecards_scorecardkpi_1.kpi = importer.locate_object(KPI, "id", KPI, "id", 3, {})
    scorecards_scorecardkpi_1.score = Decimal('0.80')
    scorecards_scorecardkpi_1 = importer.save_or_locate(scorecards_scorecardkpi_1)

    scorecards_scorecardkpi_2 = ScorecardKPI()
    scorecards_scorecardkpi_2.created = dateutil.parser.parse("2017-03-31T13:34:08.040886+00:00")
    scorecards_scorecardkpi_2.modified = dateutil.parser.parse("2017-04-08T11:07:52.299964+00:00")
    scorecards_scorecardkpi_2.scorecard = scorecards_scorecard_1
    scorecards_scorecardkpi_2.kpi = importer.locate_object(KPI, "id", KPI, "id", 1, {})
    scorecards_scorecardkpi_2.score = Decimal('1.20')
    scorecards_scorecardkpi_2 = importer.save_or_locate(scorecards_scorecardkpi_2)

    scorecards_scorecardkpi_3 = ScorecardKPI()
    scorecards_scorecardkpi_3.created = dateutil.parser.parse("2017-04-12T06:04:09.774342+00:00")
    scorecards_scorecardkpi_3.modified = dateutil.parser.parse("2017-04-12T06:04:09.774399+00:00")
    scorecards_scorecardkpi_3.scorecard = scorecards_scorecard_1
    scorecards_scorecardkpi_3.kpi = importer.locate_object(KPI, "id", KPI, "id", 2, {})
    scorecards_scorecardkpi_3.score = Decimal('0.00')
    scorecards_scorecardkpi_3 = importer.save_or_locate(scorecards_scorecardkpi_3)

    scorecards_scorecardkpi_4 = ScorecardKPI()
    scorecards_scorecardkpi_4.created = dateutil.parser.parse("2017-04-12T06:30:16.328644+00:00")
    scorecards_scorecardkpi_4.modified = dateutil.parser.parse("2017-04-12T06:30:16.328711+00:00")
    scorecards_scorecardkpi_4.scorecard = scorecards_scorecard_2
    scorecards_scorecardkpi_4.kpi = importer.locate_object(KPI, "id", KPI, "id", 8, {})
    scorecards_scorecardkpi_4.score = Decimal('0.00')
    scorecards_scorecardkpi_4 = importer.save_or_locate(scorecards_scorecardkpi_4)

    scorecards_scorecardkpi_5 = ScorecardKPI()
    scorecards_scorecardkpi_5.created = dateutil.parser.parse("2017-04-12T06:31:08.708422+00:00")
    scorecards_scorecardkpi_5.modified = dateutil.parser.parse("2017-04-12T06:31:08.708487+00:00")
    scorecards_scorecardkpi_5.scorecard = scorecards_scorecard_2
    scorecards_scorecardkpi_5.kpi = importer.locate_object(KPI, "id", KPI, "id", 9, {})
    scorecards_scorecardkpi_5.score = Decimal('0.00')
    scorecards_scorecardkpi_5 = importer.save_or_locate(scorecards_scorecardkpi_5)

    scorecards_scorecardkpi_6 = ScorecardKPI()
    scorecards_scorecardkpi_6.created = dateutil.parser.parse("2017-04-12T06:32:14.534735+00:00")
    scorecards_scorecardkpi_6.modified = dateutil.parser.parse("2017-04-12T06:32:14.534801+00:00")
    scorecards_scorecardkpi_6.scorecard = scorecards_scorecard_2
    scorecards_scorecardkpi_6.kpi = importer.locate_object(KPI, "id", KPI, "id", 10, {})
    scorecards_scorecardkpi_6.score = Decimal('0.00')
    scorecards_scorecardkpi_6 = importer.save_or_locate(scorecards_scorecardkpi_6)

    scorecards_scorecardkpi_7 = ScorecardKPI()
    scorecards_scorecardkpi_7.created = dateutil.parser.parse("2017-04-12T06:33:50.536393+00:00")
    scorecards_scorecardkpi_7.modified = dateutil.parser.parse("2017-04-12T06:33:50.536491+00:00")
    scorecards_scorecardkpi_7.scorecard = scorecards_scorecard_2
    scorecards_scorecardkpi_7.kpi = importer.locate_object(KPI, "id", KPI, "id", 11, {})
    scorecards_scorecardkpi_7.score = Decimal('0.00')
    scorecards_scorecardkpi_7 = importer.save_or_locate(scorecards_scorecardkpi_7)

    scorecards_scorecardkpi_8 = ScorecardKPI()
    scorecards_scorecardkpi_8.created = dateutil.parser.parse("2017-04-12T06:35:23.992189+00:00")
    scorecards_scorecardkpi_8.modified = dateutil.parser.parse("2017-04-12T06:35:23.992283+00:00")
    scorecards_scorecardkpi_8.scorecard = scorecards_scorecard_2
    scorecards_scorecardkpi_8.kpi = importer.locate_object(KPI, "id", KPI, "id", 4, {})
    scorecards_scorecardkpi_8.score = Decimal('0.00')
    scorecards_scorecardkpi_8 = importer.save_or_locate(scorecards_scorecardkpi_8)

    scorecards_scorecardkpi_9 = ScorecardKPI()
    scorecards_scorecardkpi_9.created = dateutil.parser.parse("2017-04-12T06:42:54.280869+00:00")
    scorecards_scorecardkpi_9.modified = dateutil.parser.parse("2017-04-12T06:42:54.280956+00:00")
    scorecards_scorecardkpi_9.scorecard = scorecards_scorecard_2
    scorecards_scorecardkpi_9.kpi = importer.locate_object(KPI, "id", KPI, "id", 5, {})
    scorecards_scorecardkpi_9.score = Decimal('0.00')
    scorecards_scorecardkpi_9 = importer.save_or_locate(scorecards_scorecardkpi_9)

    # Processing model: scorecards.models.Initiative

    # from scorecards.models import Initiative

    # Re-processing model: scorecards.models.Scorecard

    # scorecards_scorecard_1.kpis.add(importer.locate_object(KPI, "id", KPI, "id", 3, {}))
    # scorecards_scorecard_1.kpis.add(importer.locate_object(KPI, "id", KPI, "id", 1, {}))
    # scorecards_scorecard_1.kpis.add(importer.locate_object(KPI, "id", KPI, "id", 2, {}))

    # scorecards_scorecard_2.kpis.add(importer.locate_object(KPI, "id", KPI, "id", 8, {}))
    # scorecards_scorecard_2.kpis.add(importer.locate_object(KPI, "id", KPI, "id", 9, {}))
    # scorecards_scorecard_2.kpis.add(importer.locate_object(KPI, "id", KPI, "id", 10, {}))
    # scorecards_scorecard_2.kpis.add(importer.locate_object(KPI, "id", KPI, "id", 11, {}))
    # scorecards_scorecard_2.kpis.add(importer.locate_object(KPI, "id", KPI, "id", 4, {}))
    # scorecards_scorecard_2.kpis.add(importer.locate_object(KPI, "id", KPI, "id", 5, {}))

    # Re-processing model: scorecards.models.Evidence

    # Re-processing model: scorecards.models.Score

    # Re-processing model: scorecards.models.ScorecardKPI

    # Re-processing model: scorecards.models.Initiative
