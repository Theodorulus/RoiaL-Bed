import pytest
from client import client_no_login, client
from flask import jsonify
import json

user_data = {
    'username': 'test_user',
    'password': 'test_pass'
}

def test_register_fail(client_no_login):
    request_with_user = client_no_login.post('/auth/register', data={'username': "test_user"}, follow_redirects=True)
    request_with_pass = client_no_login.post('/auth/register', data={'password': "test_pass"}, follow_redirects=True)
    
    assert request_with_user.status_code == 400
    assert request_with_pass.status_code == 400
    assert json.loads(request_with_user.data.decode())["status"] == 'Password is required.'
    assert json.loads(request_with_pass.data.decode())["status"] == 'Username is required.'

def test_register_existing_account(client_no_login):
    client_no_login.post('/auth/register', data=user_data, follow_redirects=True)
    request = client_no_login.post('/auth/register', data=user_data, follow_redirects=True)

    assert request.status_code == 409

def test_register_success(client_no_login):
    request = client_no_login.post('/auth/register', data=user_data, follow_redirects=True)
    assert request.status_code == 200
    assert json.loads(request.data.decode())["status"] == 'User registered succesfully'

def test_login_fail(client_no_login):
    client_no_login.post('/auth/register', data=user_data, follow_redirects=True)
    request = client_no_login.post('/auth/login', data={}, follow_redirects=True)
    assert request.status_code == 400
    assert json.loads(request.data.decode())["status"] == 'Username is required.'

def test_login_not_found(client_no_login):
    request = client_no_login.post('/auth/login', data=user_data, follow_redirects=True)
    assert request.status_code == 404
    assert json.loads(request.data.decode())["status"] == 'User not found'

def test_login_bad_credentials(client_no_login):
    client_no_login.post('/auth/register', data=user_data, follow_redirects=True)
    bad_user_data = {
        'username': user_data['username'],
        'password': 'wrong_pass'
    }
    request = client_no_login.post('/auth/login', data=bad_user_data, follow_redirects=True)
    assert request.status_code == 401
    assert json.loads(request.data.decode())["status"] == 'Username of password is incorrect'

def test_login_success(client_no_login):
    client_no_login.post('/auth/register', data=user_data, follow_redirects=True)
    request = client_no_login.post('/auth/login', data=user_data, follow_redirects=True)
    assert request.status_code == 200
    assert json.loads(request.data.decode())["status"] == 'User logged in succesfully'

def test_logout(client):
    request = client.get('/auth/logout')
    assert request.status_code == 200
    assert json.loads(request.data.decode())["status"] == 'User logged out succesfully'
