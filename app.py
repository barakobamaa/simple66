from flask import Flask, flash, request, redirect, url_for,render_template
from werkzeug.utils import secure_filename
import os.path
from tensorflow.keras.models import load_model
import cv2
import gdown
import pandas as pd
import matplotlib.pyplot as plt
from random import  randrange
import numpy as np

if(os.path.isfile('model/model_a.h5')):
    print('model exists')

else:
    print('model not found')
    url = 'https://drive.google.com/file/d/1GcQPYNy7hWzj7X0nUtYbgVbIoVs0DjYc/view?usp=sharing'
    output = 'model/model_a.h5'
    gdown.download(url, output, quiet=False) 
    print('model downloaded')

UPLOAD_FOLDER = '/uploads'
ALLOWED_EXTENSIONS = { 'jpg'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def pred_img(img_dir):
    # چک کردن اینکه ایا مدل قبلا دانلود شده یا نه
    # اگر نبود دانلود شود

    image_size = 256
    
    model = load_model('model/model_a.h5')
    

    #pic_file_name =  "243.jpg"
    #DATADIR = "/content/drive/My Drive/Kaggle/cepha400/cepha400/{}".format(pic_file_name)
    
    non_square_image = cv2.imread("input/{}".format(img_dir) ,cv2.IMREAD_GRAYSCALE)  # convert to array'
    
    
    #           -----    --- تغییرات برای خوراندن به مدل
    #   تغییرات کنتراست
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
    enhanced_contrast_img = clahe.apply(non_square_image)
    enhanced_contrast_img = non_square_image
    
    #--------    مربع کردن تصویر
    color = [0, 0, 0]
    print('tul= {}  arz={}'.format(enhanced_contrast_img.shape[0],enhanced_contrast_img.shape[1]))
    if(enhanced_contrast_img.shape[0]>enhanced_contrast_img.shape[1]):
      k=256/enhanced_contrast_img.shape[0]
      delta=enhanced_contrast_img.shape[0]-enhanced_contrast_img.shape[1]
      square = cv2.copyMakeBorder(enhanced_contrast_img, 0, 0, 0, delta, cv2.BORDER_CONSTANT,value=color)
      print('1')
    
    if(enhanced_contrast_img.shape[1]>enhanced_contrast_img.shape[0]):
      k=256/enhanced_contrast_img.shape[1]
      delta=enhanced_contrast_img.shape[1]-enhanced_contrast_img.shape[0]
      square = cv2.copyMakeBorder(enhanced_contrast_img, 0, delta,  0,0, cv2.BORDER_CONSTANT,value=color)
      print('2')
    
    if(enhanced_contrast_img.shape[1]==enhanced_contrast_img.shape[0]):
      k=256/enhanced_contrast_img.shape[1]
      delta=enhanced_contrast_img.shape[1]-enhanced_contrast_img.shape[0]
      square = cv2.copyMakeBorder(enhanced_contrast_img, 0, delta,  0,0, cv2.BORDER_CONSTANT,value=color)
      print('3')
    
    resized_square = cv2.resize(square, (image_size, image_size))  # resize to normalize data size
    reshaped_square = resized_square.reshape(-1,image_size,image_size, 1)
    # --------------------------------------------------------------------------
    #           پیش بینی
    first_prediction = model.predict([reshaped_square])
    
    
    #arz_correct = train_data_all.loc[train_data_all['image_path'] == pic_file_name][stp[0]]
    #tul_correct = train_data_all.loc[train_data_all['image_path'] == pic_file_name][stp[1]]
    #print(tul_correct)
    #print(arz_correct)
    
    
    first_arz=first_prediction[0][0]/k
    first_tul=first_prediction[0][1]/k
    print("predict: arz= {} tul= {}".format(first_arz,first_tul))
    #print("CORRECT: arz_correct= {} tul_correct= {}".format(arz_correct,tul_correct))
    
    plt.figure(figsize = (7,7))
    
    plt.scatter(first_arz,first_tul,color='r')
    
    plt.imshow(square, cmap='gray')  # graph it

    pred_dir='static/{}'.format(img_dir)
    plt.savefig(pred_dir)
     
    return img_dir





def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            print(filename)
            rand_name = randrange(999)
            img_dir = '{}.jpg'.format(rand_name)
            file.save(os.path.join('input',img_dir))

            pred_dir = pred_img(img_dir)
            out_img_path='/static/{}'.format(pred_dir)
            return render_template("resault.html", user_image = out_img_path)

                   
         
    return '''
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload new File</h1>
    <form method=post enctype=multipart/form-data>
      <input type=file name=file>
      <input type=submit value=Upload>
    </form>
    '''
    
if __name__ == "__main__":
    app.run(debug=True)    