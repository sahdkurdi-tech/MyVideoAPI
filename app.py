from flask import Flask, request, jsonify
import yt_dlp

app = Flask(__name__)

@app.route('/download', methods=['GET'])
def download_video():
    url = request.args.get('url')
    
    if not url:
        return jsonify({"error": "تکایە لینکێک بنێرە"}), 400

    # ڕێکخستنەکانی yt-dlp بۆ هێنانی باشترین کوالێتی ڤیدیۆ و دەنگ پێکەوە
    ydl_opts = {
        'format': 'best',
        'quiet': True,
        'no_warnings': True,
        'nocheckcertificate': True
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            
            # زانیارییەکان دەردەهێنین
            video_url = info.get('url')
            title = info.get('title', 'Video')
            
            # وەڵامەکە بە فۆرماتی JSON بۆ ئایفۆنەکە دەنێرینەوە
            return jsonify({
                "success": True,
                "title": title,
                "qualities": [
                    {
                        "resolution": "باشترین کوالێتی (Direct)",
                        "url": video_url
                    }
                ]
            })
            
    except Exception as e:
        return jsonify({"error": str(e), "success": False}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)