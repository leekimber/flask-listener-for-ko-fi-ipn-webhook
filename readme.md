title: readme.md

date: 2020-12-02 18:43

modified: Thu 22 Apr 2021 18:29:41 BST

tags: 

authors: Lee Kimber

summary: Usage notes for Ko-fi IPN listener

These files were ripped from a bigger, working system and have been whitewashed for general purpose use. They have not been tested in their current form.

They are, however, full of inspection code and console statements to help examine how IPN post content looks. Also to parse the data and respond with json or save the data to a database. 

- ko-fi_flask_route.py: The core flask route file.

- functions.py: Contains a very full request processing function (process_submission()), a mongodb connection function (mongodb_conn()) and a get_payments_data() function to add payment from the Ko-fi IPN webhook to a database.

- config.py: Contains configuration data used by both scripts.


