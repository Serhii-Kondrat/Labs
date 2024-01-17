import os
from flask import render_template, redirect, url_for, request, abort
from datetime import datetime
from . import portfolio

@portfolio.route('/')
def home():
    osInfo = os.environ.get('OS')
    agent = request.user_agent
    time = datetime.now().strftime("%H:%M:%S")
    
    return render_template('home.html', agent=agent, time=time, osInfo=osInfo)


@portfolio.route('/page1')
def page1():
    osInfo = os.environ.get('OS')
    agent = request.user_agent
    time = datetime.now().strftime("%H:%M:%S")
    return render_template('page1.html', agent=agent, time=time, osInfo=osInfo)

@portfolio.route('/page2')
def page2():
    osInfo = os.environ.get('OS')
    agent = request.user_agent
    time = datetime.now().strftime("%H:%M:%S")
    return render_template('page2.html', agent=agent, time=time, osInfo=osInfo)

@portfolio.route('/page3')
def page3():
    osInfo = os.environ.get('OS')
    agent = request.user_agent
    time = datetime.now().strftime("%H:%M:%S")
    return render_template('page3.html', agent=agent, time=time, osInfo=osInfo)

@portfolio.route('/about')
def about():
    osInfo = os.environ.get('OS')
    agent = request.user_agent
    time = datetime.now().strftime("%H:%M:%S")
    return render_template('about.html', agent=agent, time=time, osInfo=osInfo)


