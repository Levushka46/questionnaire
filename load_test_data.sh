#!/bin/bash

python manage.py loaddata fixtures/{Page,Question,SelectOption,Survey}.json  --app formpages
