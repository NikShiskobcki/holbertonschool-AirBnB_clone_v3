#!/usr/bin/python3
"""index file"""
from api.v1.views import app_views
from flask import jsonify

@app_views.route('/status')
def status():
    """displays status"""
    dic = {"status" : "OK"}
    return jsonify(dic)
    
