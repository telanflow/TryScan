#!/usr/bin/env python
#-*- coding:utf-8 -*-
import json
from tryscan import app, login_manage
from tryscan.models import TaskQueue, User
from flask import request, render_template, jsonify, redirect, url_for
from flask_paginate import Pagination
from flask_login import login_required, login_user, logout_user, current_user

__author__ = 'try'


@login_manage.user_loader
def load_user(user_id):
    return User(user_id)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    else:
        client_id = request.values.get('client_id', False)
        if client_id:
            user = User(client_id)
            login_user(user)
            return jsonify({'status':1, 'msg':'success'})
        else:
            return jsonify({'status':0, 'msg':'error'})

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/', methods=['GET'])
@app.route('/index', methods=['GET'])
@login_required
def index():
    return render_template('index.html')

@app.route('/list', methods=['GET'])
@app.route('/list/<int:page>')
@login_required
def list(page=1):
    client_no = current_user.get_id() # 用户ID
    count = TaskQueue.query.filter_by(client_no=client_no).count()
    paginate = TaskQueue.query.filter_by(client_no=client_no).order_by(TaskQueue.id.desc()).paginate(page, app.config['PAGE_SIZE'], False)
    pagination = Pagination(page=page, total=count, per_page=app.config['PAGE_SIZE'], bs_version=3)
    list = []
    for i in paginate.items:
        try:
            i.payload = json.loads(i.payload)
        except:
            i.payload = False
        list.append(i)

    return render_template('list.html', pagination=pagination, lists=list)

@app.route('/injection', methods=['GET'])
@app.route('/injection/<int:page>')
@login_required
def injection(page=1):
    client_no = current_user.get_id() # 用户ID
    count = TaskQueue.query.filter('payload != ""').filter_by(status=1, client_no=client_no).count()
    paginate = TaskQueue.query.filter('payload != ""').filter_by(status=1, client_no=client_no).order_by(TaskQueue.id.desc()).paginate(page, app.config['PAGE_SIZE'], False)
    pagination = Pagination(page=page, total=count, per_page=app.config['PAGE_SIZE'], bs_version=3)
    list = []
    for i in paginate.items:
        try:
            i.payload = json.loads(i.payload)
        except:
            i.payload = False
        list.append(i)

    return render_template('injection.html', pagination=pagination, lists=list)

@app.route('/complete', methods=['GET'])
@app.route('/complete/<int:page>')
@login_required
def complete(page=1):
    client_no = current_user.get_id() # 用户ID
    count = TaskQueue.query.filter_by(status=1, client_no=client_no).count()
    paginate = TaskQueue.query.filter_by(status=1, client_no=client_no).order_by(TaskQueue.id.desc()).paginate(page, app.config['PAGE_SIZE'], False)
    pagination = Pagination(page=page, total=count, per_page=app.config['PAGE_SIZE'], bs_version=3)
    list = []
    for i in paginate.items:
        try:
            i.payload = json.loads(i.payload)
        except:
            i.payload = False
        list.append(i)

    return render_template('complete.html', pagination=pagination, lists=list)


@app.route('/profile')
@login_required
def profile():
    return render_template('profile.html')



# 自定义Error
@app.errorhandler(401)
@app.errorhandler(404)
@app.errorhandler(500)
def internal_server_error(error):
    return render_template('error/404.html'), 404