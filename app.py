from flask import Flask, Response, request, render_template
import requests

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/watch')
def watch():
    video_url = request.args.get('url')
    if not video_url:
        return "Error: No video URL provided", 400
    return render_template('watch.html', video_url=video_url)

@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/stream')
def stream():
    video_url = request.args.get('url')
    if not video_url:
        return "Error: No video URL provided", 400

    # Set range headers for chunked streaming
    headers = {'Range': request.headers.get('Range', 'bytes=0-')}
    response = requests.get(video_url, headers=headers, stream=True)

    # Check if the response supports Range requests
    if response.status_code == 416:
        return "Error: Requested Range not satisfiable", 416

    # Stream the content
    return Response(
        response.iter_content(chunk_size=1024),
        content_type=response.headers.get('Content-Type', 'video/mp4'),
        status=response.status_code,
        headers={key: value for key, value in response.headers.items() if key.lower().startswith('content-')}
    )

if __name__ == '__main__':
    app.run(debug=True)
