
# Ochenil

This online application is designed to handle everything regarding a pet boarding. You can connect as a customer to book a stay for your dog and you can connect as the pet boarding owner to administrate everything

## Project scructure
Ochenil is a django app wrote in python following a MVT architecture. It uses bootstrap for the frontend. 

The project contains 4 apps:
- authentication (user signin/signup)
- customer (list of my saved dogs, of my saved bookings, add a new dog)
- administration (display of all bookings for the pet boarding, declare box unavailability, booking cancellation, display daily capacity for both big and small dogs)
- generic (manage website menu and main page content etc)

## Virtual Environment
To avoid any unnecessary configuration, we suggest that you name your virtual  environment folder: **OChenil_env**. Using another denomination will not create errors but some parameters (like the exclusion of this folder for the tests) will have to be resetted manually

## Environment variables:
In order for this project to run, you need some environment variables.
The ones you need are all listed in the example.env file, please update this file with your database credentials and django secret key and then save it under the ".env" name.
  

## *Database connection parameters:*

Regarding the connection to your database, **please replace the values in the "DB credentials section of the example.env file** and then rename/setup this file to use it as source for your project environment variables.

  
## Requirements:

All required packages to run this app are listed in the requirements.txt file.

To install all requidred packages, please run

    pip install -r requirements.txt


## *Tests*


### Run all tests (recommended)

use the following command:

    python manage.py test

  

### Run functionnal tests only

For functionnal tests only regarding the *authentication* app:

    python manage.py test authentication.tests.tests_functionnals

  

For functionnal tests only regarding the *administration* app:

    python manage.py test administration.tests.tests_functionnals


For functionnal tests only regarding the *customer* app:

    python manage.py test customer.tests.tests_functionnals

  

### Run unit tests only

For unit tests only regarding the administration app:

    python manage.py test administration.tests.tests_unit

For unit tests only regarding the customer app:

    python manage.py test customer.tests.tests_unit

  
  

### *Tests coverage report*


To get a coverage report, please run

    coverage run manage.py test

And then:

    coverage report

  

*information:* the coverage report configuration is set in rootfolder in .coveragerc file, it excludes all the virtual environment files located in the 'OChenil_env' directory.

  

## PEP8 compliance

Use of flake 8

There is a .flake8 configuration file in the root directory to exclude django generated files such as migrations and cache.