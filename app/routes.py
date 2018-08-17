import controllers
from flask import render_template, url_for, flash, redirect, request, jsonify, g
from flask_login import current_user, login_user, logout_user, login_required
import json
from werkzeug.security import generate_password_hash
from app import app, db
from app.models import *
from forms import LoginForm, BookForm
from flask_httpauth import HTTPBasicAuth

auth = HTTPBasicAuth()




