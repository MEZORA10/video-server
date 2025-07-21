from flask import Flask, request, jsonify
import yt_dlp

app = Flask(__name__)

@app.route('/getvideo', methods=['POST'])
def get_video():
    data = request.get_json()
    video_url = data.get('url')

    if not video_url:
        return jsonify({'error': 'رابط غير موجود'}), 400

    try:
        ydl_opts = {
            'format': 'bestvideo+bestaudio/best',
            'quiet': True,
            'noplaylist': True
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(video_url, download=False)
            return jsonify({
                'title': info.get('title'),
                'url': info.get('url')
            })

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
