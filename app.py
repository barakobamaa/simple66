from flask import Flask

app = Flask(__name__)

@app.route('/')
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
            #img_dir = '{}.jpg'.format(rand_name)
            #file.save(os.path.join('input',img_dir))

            #pred_dir = pred_img(img_dir)
            #out_img_path='/static/{}'.format(pred_dir)
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