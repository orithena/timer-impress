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
from random import randint
import math
        
app = Flask(__name__)
genshi = Genshi(app)

handlers = {}

def handler_for(preset):
  def gethandler(f):
    handlers[preset] = f
    return f
  return gethandler

@handler_for('screw')
def preset_screw(time, step):
  # This is where the time slide parameters are generated as a function of the slide number.
  # Each generated tuple has the format (slidenumber, posx, posy, posz, rotx, roty, rotz, scale, time_as_string)
  # Play with the factors of a, but not with the string :)
  return [ (a, math.sin(a)*200, a*300, a*300, a*9, a*9, a*9, 1, "%s:%02d" % ( ((a*step)/60), ((a*step) % 60) ),) for a in xrange(time/step, -1, -1) ]

@handler_for('hoparound')
def preset_hoparound(time, step):
  return [ (a, math.sin(a)*500, math.cos(a)*500, a*500, a*12, a*12, a*12, 1, "%s:%02d" % ( ((a*step)/60), ((a*step) % 60) ),) for a in xrange(time/step, -1, -1) ]

@handler_for('random')
def preset_random(time, step):
  c = ( randint(-500, 1500), randint(-500,1500), randint(-500, 1500), randint(-90, 90), randint(-90, 90), randint(-90, 90), randint(-768, 768)/256.0 )
  return [ (a, a*c[0], a*c[1], a*c[2], a*c[3], a*c[4], a*c[5], 1, "%s:%02d" % ( ((a*step)/60), ((a*step) % 60) ),) for a in xrange(time/step, -1, -1) ]

@handler_for('linear')
def preset_test(time, step):
  return [ (a, 0, a*380, a*1000, 0, 0, 0, 1, "%s:%02d" % ( ((a*step)/60), ((a*step) % 60) ),) for a in xrange(time/step, -1, -1) ]

@handler_for('test')
def preset_test(time, step):
  return [ (a, a*10, a*40, a*100, a*3, a*6, a*8, 1, "%s:%02d" % ( ((a*step)/60), ((a*step) % 60) ),) for a in xrange(time/step, -1, -1) ]

@app.route('/')
def welcome():
  return render_template('index.html', {'slide_params': [], 'presets': handlers.keys() })
  
@app.route('/<int:time>')
@app.route('/<int:time>/<int:step>')
@app.route('/<int:time>/<int:step>/<preset>')
@app.route('/<int:time>/<int:step>/<preset>/<sound>')
def index(time=300, step=5, preset='screw', sound='nosound'):
  sound = not (sound == "nosound")
  if step < 2:
    step = 2
  slide_params = handlers[preset](time, step)
  return render_template('index.html', {'slide_params': slide_params, 'sound': sound, 'step': step })
  

if __name__ == '__main__':
  app.run(host='0.0.0.0', debug=True)
        