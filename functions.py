#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#: File Name : functions.py
#: Creation Date : 29-04-2019
#: Last Modified : Wed 02 Dec 2020 06:01:46 PM UTC
#: Created By : Lee Kimber <info@12voltfarm.com>
#
################################
"""
    Purpose: Separates functions from routes

    Further develop as a package using:
    https://timothybramlett.com/How_to_create_a_Python_Package_with___init__py.html
    as a guide
"""

import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import config
import pymongo  # per tests for https://stackoverflow.com/questions/28113947/how-to-properly-use-try-except-in-python
from pymongo import MongoClient


# Define functions


def mongodb_conn():
    """
        Function: Generalised mongodb connection creator
        From:
        https://stackoverflow.com/questions/28113947/how-to-properly-use-try-except-in-python
        Params: output: connection object

        From:
        https://stackoverflow.com/questions/28113947/how-to-properly-use-try-except-in-python
    """
    try:
        return MongoClient(config.PAMONGODB_HOST, config.PAMONGODB_PORT)
    except pymongo.errors.ConnectionFailure, e:
        return "%s" % e


def process_submission(request):
    """
    Function: Universal submission processing function
    Params: Input: request object
    Params: Output: dictionary of filled fields, excluding blank fields
    Usage: Set up to ease debugging. It's been tested against various
        submission code and builds the experience into its 'if' tree. However,
        turning debugging to 1 to examine any request objects it struggles with.
    """

# Set up environment
    debug = 1
    filled_form_fields = {}

# Start reporting what is being processed:
    if debug == 1:
        print("DEBUGGING initial request in function")
        print(request)
# Process the input data and - to help users debug new IPN posts - report on content:
# A functionable sequence starts here. Test separating it out sometime
        print("debugging: a submission attempt.")
        if len(request.data) > 0:
            print("DEBUGGING: There is request.data")
            print("DEBUGGING: Apparently a raw submission attempt:")
            submission_type = 'unsure'
        if len(request.form) > 0:
            print("DEBUGGING: There is request.form")
            print("DEBUGGING: Apparently a Webform submission attempt:")
            submission_type = 'webform'
        if request.is_json:
            print("DEBUGGING: There is a request.is_json object")
            submission_type = 'json'
        if request.args:
            print("DEBUGGING: There is a request.args object")
            submission_type = 'args'

# Try to figure out what format the posted data is in
    if request.json:
        if len(request.json) > 0:
            submission_type = 'json'
            filled_form_fields = request.json
            if debug == 1:
                print("DEBUGGING: Processing the request.json object")
                print(request.json)
    elif len(request.form) > 0:
        submission_type = 'webform'
        form_data = request.form.to_dict()
        if debug == 1:
            print("DEBUGGING: Processing request.form")
            print("DEBUGGING: showing form_data contents:")
        for form_key in form_data.keys():
            if len(form_data[form_key]) > 0: 
                filled_form_fields[form_key] = form_data[form_key]
                if debug == 1:
                    print(form_key + ": " + str(form_data[form_key]))
    elif request.args:
        if debug == 1:
            print("DEBUGGING: Processing request.args")
            print("DEBUGGING: Apparently a content-type unspecified submission attempt:")
        filled_form_fields = request.args.to_dict()
        submission_type = 'not sure but request.args has content'
# We now have a form_data dict with keys, values where values exist
# But... some javascript posts are none of the above request.json, request.form, or request.args
    elif len(request.data) > 0:  # ie we didn't get anything from json or the request.form so we try manual parsing
        submission_type = 'json'
        if debug == 1:
            print("DEBUGGING: There is request.data. Processing it into request.form")
            print("DEBUGGING: Presumably a JavaScript submission attempt:")
# If we do have request.data, anticipate using split to break up the request.data string
        string_args = request.data[2:-2]  # get rid of the string's terminating {" and "}
        form_data = dict(pair.split('":"') for pair in string_args.split('","'))
        for form_key in form_data.keys():
            if len(form_data[form_key]) > 0: 
                filled_form_fields[form_key] = form_data[form_key]
                if debug == 1:
                    print(form_key + ": " + str(form_data[form_key]))
    else:
        print("DEBUGGING: There is apparently no request.data.")
        submission_type = 'Lord knows'

# We now have a form_data dict with keys, values where values exist
    if debug == 1:
        print("DEBUGGING: submission_type: " + submission_type)
        if len(filled_form_fields) > 0:
            print(filled_form_fields)
        else:
            print("No filled_form_fields obtained")

    return filled_form_fields


def get_payments_data():
    """
        Function: get payments data for all payments in members.payments
        Params: output: payments collection 

    """
    connection = mongodb_conn()
    if connection is None:
        return {'status': "error", 'message': "No connection object from db server"}
    elif isinstance(connection, str):
        return {'status': "error", 'message': "Database call returned: '" + connection + "'"}
    elif isinstance(connection, dict):
        return {'status': "error", 'message': "Database call returned: '" + connection + "'"}
    else:
        try:
            payments_collection = connection[config.PAYMENTSDB][config.PAYMENTS_COLLECTION]
            connection.close()
        except:
            return {'status': "error", 'message': "Collection: '" + PAYMENTS_COLLECTION + "' not found"}

    return payments_collection


def main():
    """
    Function: Set of routines to test this script's functions
    """
# ToDo:
#    Tests for:
#    mongodb_conn()
#    process_submission()
#    get_payments_data()

    print("Write some tests") 

# End define functions

if __name__ == '__main__':

    main()

