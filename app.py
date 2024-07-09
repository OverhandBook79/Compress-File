from flask import Flask, request, redirect, send_file, render_template
import zlib
import os

app = Flask(__name__)

def compress_file_to_1kb(file_data):
    compressed_data = zlib.compress(file_data, level=9)
    
    if len(compressed_data) > 1024:
        compressed_data = compressed_data[:1024]
    
    return compressed_data

@app.route('/')
def index():
    return render_template('index.html', compressed_file_url=None)

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return redirect('/')
    
    file = request.files['file']
    
    if file.filename == '':
        return redirect('/')
    
    file_data = file.read()
    
    if len(file_data) > 1 * 1024 * 1024 * 1024:  # 1 GB in bytes
        return "File size exceeds 1 GB.", 400
    
    compressed_data = compress_file_to_1kb(file_data)
    
    compressed_file_path = 'compressed_file.bin'
    with open(compressed_file_path, 'wb') as f:
        f.write(compressed_data)
    
    return render_template('index.html', compressed_file_url='/download')

@app.route('/download')
def download_file():
    compressed_file_path = 'compressed_file.bin'
    return send_file(compressed_file_path, as_attachment=True)

if __name__ == "__main__":
    app.run(debug=True)
