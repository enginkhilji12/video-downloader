from flask import Flask, request, send_file
import yt_dlp
import os
import glob

app = Flask(__name__)
TEMP_FOLDER = "./downloads/"
os.makedirs(TEMP_FOLDER, exist_ok=True)

@app.route('/')
def index():
    return '''
    <html><body>
    <h2>Video Downloader</h2>
    <form method="POST" action="/download">
    <input name="url" placeholder="Paste video URL" required style="width:300px;">
    <button type="submit">Download</button>
    </form>
    </body></html>
    '''

@app.route('/download', methods=['POST'])
def download():
    url = request.form['url']

    for f in glob.glob(TEMP_FOLDER + '*'):
        try:
            os.remove(f)
        except:
            pass

    ydl_opts = {
        'outtmpl': TEMP_FOLDER + '%(title).100s.%(ext)s',
        'format': 'mp4',
        'quiet': True,
        'postprocessors': [{
            'key': 'FFmpegVideoConvertor',
            'preferedformat': 'mp4',
        }],
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info)
        return send_file(filename, as_attachment=True)
    except Exception as e:
        return f"<h3 style='color:red;'>Error: {e}</h3>"

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080)
