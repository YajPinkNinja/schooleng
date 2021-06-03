from flask import Flask, render_template, request, redirect
import serial
from colorama import init
from colorama import Fore, Back, Style
import threading
import time
temp = "NaN"
humid = "NaN"
rotstatetemp = "off"
rotstate = 'off'
app = Flask(__name__)
app.config['TEMPLATES_AUTO_RELOAD'] = True
if __name__ == '__main__':
    ser = serial.Serial('COM3',9600, timeout=1)
    ser.flush()

@app.route('/')
def hello_world():
    author = "Zepje"
    name = "ZEPJEPLA"
    data = ser.readline().decode('utf-8')
    ser.flushInput() #flushes serial input so it doesn't have old messages stuck in it.
    #print(data)
    x = data.split(',')
    temp = int(float(x[2])*100)/100
    humid = int(float(x[1])*100)/100
    #print(temp)
    #print(humid)
    return render_template('index.html', author=author, name=name,temp=round(temp,2), humid=round(humid))

@app.route('/signup', methods = ['POST'])
def signup():
    text = request.form['text']
    print(text)
    if text != "":
        ser.write(str(text+"\n").encode('utf-8'))
    people = request.form.getlist('rot')
    if "on" in people:
        print("succes!")
    #    rotstatetemp = "on"
        ser.write(str('99'+"\n").encode('utf-8'))
         
    else:
        ser.write(str('100'+"\n").encode('utf-8'))
        print("fail :(")
    #    rotstatetemp = "off"
    #print(people)
    return redirect('/')


    
    
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=81, )