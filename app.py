import os, glob
from flask import Flask, render_template, redirect, flash, request, send_from_directory, url_for
from werkzeug.utils import secure_filename
from utils import *
from datetime import datetime


app = Flask(__name__,static_url_path='/Static')
app.config['UPLOADS_FOLDER'] = UPLOADS_FOLDER
app.config['DOWNLOADS_FOLDER'] = DOWNLOADS_FOLDER
app.config['SECRET_KEY'] = 'my secret'

@app.route('/', methods=["GET", "POST"])
def index():
    if request.method == "GET":
        return render_template('index.html')
        if not 'file' in request.files:
            flash('No file selected!')
            return redirect(request.url)

    file = request.files.get('file')
    if file.filename == '':
        flash('No file uploaded')
        return redirect(request.url)
    
    if file_valid(file.filename):
      filename = file.filename
      dateTimeObj = datetime.now().strftime("%y-%m-%d %H-%M-%S")
      filename = filename.split(".")
      filename = filename[0]+dateTimeObj+"."+filename[1]
      filename = secure_filename(filename)
      file.save(os.path.join(app.config['UPLOADS_FOLDER'], filename))
      flash("Files uploaded successfully")

      # return redirect(request.url)
      return redirect(url_for('download'))
    else:
      flash('Invalid file type')
      return redirect(request.url) 
      
# @app.route('/Predictions/<path:filename>')
# def send_attachment(filename):
#   return send_from_directory(app.config['DOWNLOADS_FOLDER'], 
#     filename=filename, as_attachment=True)

@app.route("/download")
def download():

  # Get latest file from folder
  list_of_files = glob.glob(r'C:\Users\darsh\Desktop\Darshan\AIP\Project\Project APS\Front_end\Predictions\*')
  latest_file = max(list_of_files, key = os.path.getctime)
  latest_file = os.path.basename(latest_file)
  print(latest_file)
  #os.listdir('Predictions')
  return render_template('download.html',filename = latest_file)

@app.route("/download/<filename>")
def download_file(filename):
  return send_from_directory('Predictions',filename)


if __name__ == '__main__':
    app.run(debug=True)