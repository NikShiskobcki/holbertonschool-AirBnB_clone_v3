#!/usr/bin/python3
"""index file"""
from api.v1.views import app_views
from flask import Flask

@app_views.route('/status, strict_slashes=False')
def status():
    """displays status"""
    return('"status": "OK"'.json())
