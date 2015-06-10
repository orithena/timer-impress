# -*- coding: utf-8 -*-

import os
import sys
workdir = os.path.dirname(__file__)
from flask import Flask
from flaskext.genshi import Genshi, render_template
from genshi.template import MarkupTemplate 
from genshi.template import TemplateLoader
from genshi import Stream  
from genshi.input import XML
from genshi.core import QName
import os.path
import logging
        
app = Flask(__name__)
genshi = Genshi(app)

@app.route('/')
@app.route('/<time>')
def index(time=300):
  try:
    time=int(time)
  except:
    time=300
  # This is where the time slide parameters are generated as a function of the slide number.
  # Each generated tuple has the format (slidenumber, posx, posy, posz, rotx, roty, rotz, scale, time_as_string)
  # Play with the factors of a, but not with the string :)
  slide_params = [ (a, 0, a*100, a*100, a*6, a*6, a*6, 1, "%s:%02d" % ( ((a*5)/60), ((a*5) % 60) ),) for a in xrange(time/5, -1, -1) ]
  return render_template('index.html', {'slide_params': slide_params,});

if __name__ == '__main__':
  app.run(host='0.0.0.0', debug=True)
        