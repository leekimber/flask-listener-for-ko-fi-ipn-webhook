#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#: File Name : config.py
#: Creation Date : 06-02-2019
#: Last Modified : Wed 02 Dec 2020 06:15:52 PM UTC
#: Created By : Lee Kimber <info@12voltfarm.com>
#: Per 
#: https://scotch.io/tutorials/getting-started-with-flask-a-python-microframework
################################
"""
    Purpose: manageable config for flask IPN payments API
""" 

# Enable Flask's debugging features. Should be False in production
DEBUG = True
SECRET_KEY = 'My Precious'

# Flask run conditions
# You can test with self-signed keys if https is being used
SSL_CONTEXT = ('fullchain.pem', 'privkey.pem')

# Variables
API_VERSION = '/api/v1.0'

# Main payments database
PAMONGODB_HOST = '192.168.2.142'
PAMONGODB_PORT = 27017
PAYMENTSDB = 'subscribers'
PAYMENTS_COLLECTION = 'payments'

