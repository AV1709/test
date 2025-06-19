# -*- coding: utf-8 -*-

from flask import (
    Blueprint, flash, redirect, render_template, request, url_for,session
)
import os

import speech_recognition as sr

import json

bp = Blueprint('blog', __name__)


standard_texts =[]
global output
output = {}

global file_path
file_path = ""
output2 = ""

@bp.route('/')
def index():
    with open(os.path.dirname(os.path.realpath(__file__))+'/static/data.json', encoding='utf-8') as json_file:
        global standard_texts
        standard_texts= json.load(json_file)
        session.permanent = True
    return redirect(url_for('blog.create'))


@bp.route('/logout')
def logout():
    session.clear()
    output.clear()
    return redirect(url_for('blog.index'))

@bp.route('/printing')
def printing():
    global file_path
    file_path =  os.path.dirname(os.path.realpath(__file__))+'/'+"demofile.txt"
    with open(file_path, "w") as f:
        e3 = ''
        e4 = ''
        for key,value in output.items():
            if 'out' in key and value!= '':
                if 'e3' in key and value!= '':
                    e3 = value
                elif 'e4' in key and value!= '':
                    e4 = value
                else:
                    f.write(value+ '\n')

        if e3 != '' :
            f.write(e3 + '\n')
        if e4 != '':
            f.write(e4 + '\n')


    flash(f'Datei wurde unter {file_path} gespeichert')
    f.close()
    output.clear()
    session.clear()
    session.permanent = True
    return redirect(url_for('blog.create'))


@bp.route('/create', methods=('GET', 'POST'))
def create():
    global output
    input = {}
    if not standard_texts:
        return redirect(url_for('blog.index'))

    global r
    r = sr.Recognizer()
    global m
    m = sr.Microphone()
    with m as source:
        r.adjust_for_ambient_noise(source)  # we only need to calibrate once, before we start listening


    for i in range(1,89):
        stri = str(i * 10)

        try:
            input[stri]= session[stri]
            if session[stri] == 'unnotice': #unauffällig checked
                output[stri + 'out'] = standard_texts[stri]
                output[str(int(stri) + 1) + 'out'] = ''
            elif session[stri] == 'notice_left': #auffällig checked, aber nichts im Textfeld eingetragen
                output[stri+'out'] = ''
            else: #Inhalt im Textfeld eingetragen
                output[stri+'out'] = session[stri]
        except:
            pass

        striR = str(i*10+1)

        try:
            input[striR] = session[striR]
            if session[striR] == 'notice_right':
                output[striR+'out'] = ''
            else:
                output[striR+'out'] = session[striR]
        except:
            pass

        try:
            input['e3'] = session['e3']
            output['e3out'] = session['e3']
        except:
            pass


        try:
            input['e4'] = session['e4']
            output['e4out'] = session['e4']
        except:
            pass


    return render_template('create.html', data=input, out=output,file_path=file_path)


@bp.route('/process',  methods=(['POST']))
def process():
    global output

    if request.method == 'POST':

        name = request.form['name']
        value = request.form['value']
        if value == "unnotice":
            session[name]=value
            output[name+'out'] =  standard_texts[name]
            output[str(int(name)+1)+'out'] =  ''
        elif (value == "notice_left" or value == "notice_right"):
            session[name]=value
            output[name+'out'] =  ''
        else: #textarea, name=xxxd
            name = name.strip('d') #name = xxx
            output[name+'out'] = value
            if value != '' :
                session[name] = value

    return {"output": output}


def callback(recognizer, audio):
    # received audio data, now we'll recognize it using Google Speech Recognition
    try:
        recognized = recognizer.recognize_google(audio, language="de-DE")
        print("Google Speech Recognition thinks you said1 " + recognized)
        out= recognized
    except sr.UnknownValueError:
        print("Google Speech Recognition could not understand audio1")
        out=  ""
    except sr.RequestError as e:
        print("Could not request results from Google Speech Recognition service1; {0}".format(e))
        out= ""
    except:
        out = ""

    global output2
    output2 += out


@bp.route("/detect", methods=["POST"])
def detect():
    global stop
    global output2
    stop(wait_for_stop=False)
    returning = output2
    output2 = ''
    return {"output2": returning}


@bp.route("/record", methods=['POST'])
def record_audio():
    global r
    global m
    # start listening in the background (note that we don't have to do this inside a `with` statement)
    stop_listening = r.listen_in_background(m, callback)
    # `stop_listening` is now a function that, when called, stops background listening

    global stop
    stop = stop_listening

    print("type1: " + str(type(stop)))

    return {}
