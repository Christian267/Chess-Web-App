from flask import Flask
from flask_restful import Api, Resource, reqparse, abort, fields, marshal_with
from flask_sqlalchemy import SQLAlchemy

import config
from __main__ import api
from chessapp import dbAlchemy
from chessapp.models import HistoryModel



        