echo off
set FLASK_APP=convert.py
set FLASK_DEBUG=TRUE
echo on
flask convert %1 %2 %3