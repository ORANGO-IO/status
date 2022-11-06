#!/bin/sh

# code goes here.
wget http://flaskapp:5000/api/execute_all_jobs
echo "This is a script, run by cron!"
