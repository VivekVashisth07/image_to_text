from flask import * 
import matplotlib.image as mpimg
import matplotlib.pyplot as plt
import pytesseract as tess
import numpy as np
import pyttsx3
from gtts import gTTS
import os
import pygame
import pygame.camera
import pygame.image
from playsound import playsound
import base64
from io import BytesIO
from PIL import Image 


app = Flask(__name__) 


@app.route('/',methods=['GET'])  
def upload():  
    return render_template("file_upload_form.html")  
 
@app.route('/success', methods = ['GET','POST'])  
def success():
    #file code
    print('hello')

    if request.method == 'POST': 
        
        file = request.form['file']
        print('hi') 
        
        starter = file.find(',')
        image_data = file[starter+1:]
        image_data = bytes(image_data, encoding="ascii")
        im = Image.open(BytesIO(base64.b64decode(image_data)))
        im.save(r"app/Image/recieve1.png") 
        # file.save(r"app/Image/recieve.jpg") 
        
        # image = Image.open(r"app/Image/recieve.jpg")
        # width,height=image.size
        # new_image = image.resize((width//2, height//2))
        # new_image.save(r"app/Image/recieve.jpg")


        img = Image.open(r'app/Image/recieve1.png').convert('RGB')
        img.save(r'app/Image/recieve.jpg', 'jpeg')

        # im = Image.open(r"app/Image/recieve1.rgb")
        # rgb_im = im.convert('RGB')
        # rgb_im.save(r"app/Image/recieve.jpg")
        print('image part complete')
  

    tess.pytesseract.tesseract_cmd = '/app/.apt/usr/bin/tesseract'
    print('tesserct start')
    
    # image 
    imgpath = r"app/Image/recieve.jpg"
    print('new image')
    img=mpimg.imread(imgpath)
    #img = cv2.imread(r"{}".format(imgpath))

    config = ('-l eng --oem 1 --psm 3')

    # pytessercat
    text = tess.image_to_string(img, config=config)
    print('text form')
    print(text)

    output=(text)
    print(output)
    
    try:
        tts = gTTS(text=text, lang='en')
        tts.save(r"app/Audio/saved_file.mp3")
        print("savedd")
    except:
        return render_template("error.html")

    file=r"app/Audio/saved_file.mp3"
    result={
        "type":"audio",
        "file":file,
        }
    #playsound(file)
    #return jsonify(result)
    data=jsonify(result)
    return render_template("success.html",data=result['file'])


@app.route('/play')
def play():
    def generate():
        with open(r"app/Audio/saved_file.mp3", "rb") as fwav:
            data = fwav.read(1024)
            while data:
                yield data
                data = fwav.read(1024)
            
    #return send_file("saved_file.mp3",as_attachment=True)
    return Response(generate(), mimetype="audio/x-wav")



  

