from flask import Flask, flash, request, redirect, url_for,render_template
from werkzeug.utils import secure_filename
import os.path


UPLOAD_FOLDER = '/uploads'
ALLOWED_EXTENSIONS = { 'jpg'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

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
            #rand_name = randrange(999)
            img_dir = '77777.jpg'
            file.save(os.path.join('input',img_dir))

            #pred_dir = pred_img(img_dir)
            out_img_path='/static/{}'.format(img_dir)
            return render_template("resault.html", user_image = img_dir)

                   
         
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