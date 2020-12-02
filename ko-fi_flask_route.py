#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#: File Name : ko-fi_flask_route.py
#: Creation Date : 29-04-2019
#: Last Modified : Wed 02 Dec 2020 04:55:09 PM UTC
#: Created By : Lee Kimber <info@12voltfarm.com>
#
################################
"""
    Purpose: flask route to respond to Ko-fi payment IPN posts
"""

# IMPORTS
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import functions  # IPN-specific functions
import json
from bson.json_util import dumps
from datetime import datetime, timedelta  # timedelta only there for CORS tests
from flask import flash, Flask, jsonify, redirect, request, Response
from flask_cors import CORS
#from pymongo import MongoClient
#from flask_cors import CORS

# CONFIGURE FLASK APP
app = Flask(__name__)
# You probably won't need the below but just in case:
#CORS(app, resources={r"/*": {"origins": "*", "max_age": timedelta(days=1)}})

# Variables
debug = 1  # 0 = off, 1 = on, print stuff to console during devving/testing
app.config.from_object('config')
app.secret_key = app.config['SECRET_KEY']  # AAA test
api_version = app.config['API_VERSION']
failed_payment_redirect = 'https://your.site.com/payment_request_form.html'

# def routes:

@app.route(api_version + '/payments', methods=['POST'])
def payments():
    """
        Function: Webhook for logging payments from Ko-fi IPN
        See:
            https://ko-fi.com/manage/webhooks
        Usage:
            Create a ko-fi account
            Then test this route by logging into Ko-fi and using the 'Send Test' tool at:
            https://ko-fi.com/manage/webhooks?src=sidenmenu
    """
    if debug == 1:
        print("DEBUGGING: payment recorded at " + str(datetime.utcnow().replace(microsecond=0).isoformat()))

    metadata_dict = {
        'description': "Response to Ko-fi payment received IPN post",
    }

    if request.method != 'POST':
# Not a POST. How to handle?
# Send them to the form (currently the API version of the registration form)
#        print("DEBUGGING: a 'non-POST' payment record attempt.")
#        print(request.method)  # Help devs examine errors
        ret = {
            'status': 'error',
            'message': 'Request type should be "POST"',
            'redirect': failed_payment_redirect,
        }
        return Response(response=json.dumps(ret), status=200,
                    mimetype='application/json')
    else:
        filled_form_fields = functions.process_submission(request)
        payment_data_dict = json.loads(filled_form_fields['data'])
# From here on, we're looking at key:value pairs that came from Ko-fi's IPN post
        message_id = payment_data_dict['message_id']
        timestamp = payment_data_dict['timestamp']
        donation_type = payment_data_dict['type']
        from_name = payment_data_dict['from_name']
        message = payment_data_dict['message']
        amount = payment_data_dict['amount']
        is_public = payment_data_dict['is_public']
        url = payment_data_dict['url']

# Storing IPN data:
# Pretend we have a mongodb database called 'members' containing a collection called 'payments'
# Quick timestamp format
        datestamp = datetime.strptime(timestamp[:19], '%Y-%m-%dT%H:%M:%S')
# Common to both input types
        payments_collection = functions.get_payments_data()
        payments_collection.insert({
            'message_id': message_id, 
            'Name': from_name,
#            'Signup Date': functions.get_ko-fi_date(timestamp), # signup_date,  # Get from date now
            'Payment_date': datestamp,
            'Donation_type': donation_type,
            'Message': message,
            'Amount': amount,
        }, True)

# We don't have to respond to a Ko-fi IPN post but the below stub is there if things
# change or for other IPN cases
        if debug == 1:
            payment_data = {
                'name': from_name,
                'payment_date': timestamp,
                'donation_type': donation_type,
                'message': message,
                'amount': amount,
            }
            ret = {
                'status': 'success',
                'message': 'Inserted payment data',
                'data': payment_data,
            }
            return Response(response=json.dumps(ret), status=201,
                        mimetype='application/json')


if __name__ == "__main__":

    app.secret_key = app.config['SECRET_KEY']
    app.run(host=app.config['HOST'],port=app.config['PORT'],debug=app.config['DEBUG'], ssl_context=app.config['SSL_CONTEXT'])

