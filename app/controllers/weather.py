from flask import session, redirect, render_template, Blueprint, request, flash
from app.decorators import login_required
weather = Blueprint('weather', __name__)

@weather.route('/')
def home():
    return render_template('weather.html')
