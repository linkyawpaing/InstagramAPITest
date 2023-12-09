from flask import render_template, request, jsonify, send_file
from app import app, db, db_session
from app.models import UserToken, PhotoBook
from app.utils import fetch_photos_from_instagram, extract_hashtags_from_caption, download_photo
from app.utils import filter_photos_by_hashtag, save_photos_to_directory
import os
from collections import Counter

@app.before_first_request
def create_tables():
    """
    アプリケーションの最初のリクエストが行われる前にデータベーステーブルを作成する。
    """
    db.create_all()

@app.route('/')
def index():
    """
    アプリケーションのホームページをレンダリングする。
    """
    return render_template('index.html')

@app.route('/fetch_photos', methods=['POST'])
def fetch_photos():
    """
    Instagram APIを使用してユーザーの写真を取得し、JSON形式で返す。
    リクエストにはユーザーIDとアクセストークンが含まれる。
    取得した写真の中から、'media_type'が'IMAGE'のもののみを選択し、そのURLをリストとして返す。
    """
    USER_ID = request.json['userId']
    ACCESS_TOKEN = request.json['token']

    data = fetch_photos_from_instagram(USER_ID, ACCESS_TOKEN)

    if 'error' in data:
        return jsonify({'error': data['error']['message']})

    photos = [photo for photo in data['data'] if photo['media_type'] == 'IMAGE']
    return jsonify({'photos': photos})

@app.route('/fetch_hashtags', methods=['POST'])
def fetch_hashtags():
    """
    Instagram APIを使用してユーザーの写真からハッシュタグを抽出し、
    それらの出現回数と共にJSON形式で返す。
    リクエストにはユーザーIDとアクセストークンが含まれる。
    """
    USER_ID = request.json['userId']
    ACCESS_TOKEN = request.json['token']

    data = fetch_photos_from_instagram(USER_ID, ACCESS_TOKEN)

    if 'error' in data:
        return jsonify({'error': data['error']['message']})

    hashtags = extract_hashtags_from_caption(data)
    hashtag_counts = Counter(hashtags)
    sorted_hashtags = sorted(hashtag_counts.items(), key=lambda x: x[1], reverse=True)

    return jsonify({'hashtags': sorted_hashtags})

@app.route('/search_by_hashtag', methods=['POST'])
def search_by_hashtag():
    """
    Instagram APIを使用して特定のハッシュタグを含む写真を検索し、
    それらの写真のURLをJSON形式で返す。
    リクエストにはユーザーID、アクセストークン、検索するハッシュタグが含まれる。
    """
    USER_ID = request.json['userId']
    ACCESS_TOKEN = request.json['token']
    HASHTAG = request.json['hashtag']

    data = fetch_photos_from_instagram(USER_ID, ACCESS_TOKEN)

    if 'error' in data:
        return jsonify({'error': data['error']['message']})

    photos_with_hashtag = filter_photos_by_hashtag(data, HASHTAG)
    return jsonify({'photos': photos_with_hashtag})

@app.route('/create_photobook', methods=['POST'])
def create_photobook():
    """
    リクエストから受け取ったデータを使用して新しいフォトブックを作成し、
    成功メッセージをJSON形式で返す。
    リクエストにはフォトブックの名前、ユーザーID、写真のURLが含まれる。
    """
    data = request.json
    photobook_name = data['name']
    user_id = data['userId']
    photo_urls = save_photos_to_directory(data['photos'], user_id, photobook_name)

    PhotoBook.create_photobook(photobook_name, user_id, photo_urls)

    return jsonify({'message': 'Photobook created successfully!'})

@app.route('/get_photobooks', methods=['GET'])
def get_photobooks():
    """
    特定のユーザーIDに基づいて、そのユーザーのフォトブックのリストをJSON形式で返す。
    リクエストにはユーザーIDが含まれる。
    """
    user_id = request.args.get('userId')
    photobooks = PhotoBook.get_photobooks_by_user(user_id)
    return jsonify({'photobooks': [pb.name for pb in photobooks]})

@app.route('/get_photobook_photos', methods=['POST'])
def get_photobook_photos():
    """
    特定のフォトブック名とユーザーIDに基づいて、そのフォトブックの写真のURLをJSON形式で返す。
    リクエストにはフォトブック名とユーザーIDが含まれる。
    """
    data = request.json
    photobook = PhotoBook.get_photos_by_name_and_user(data['photobookName'], data['userId'])
    if photobook:
        photos = [os.path.basename(photo_path) for photo_path in photobook.photos]
        return jsonify({'photos': photos, 'user_id': data['userId'], 'photobook_name': data['photobookName']})
    else:
        return jsonify({'error': 'Photobook not found'}), 404

@app.route('/get_image/<user_id>/<photobook_name>/<filename>', methods=['GET'])
def get_image(user_id, photobook_name, filename):
    """
    特定のユーザーID、フォトブック名、ファイル名に基づいて、指定された画像ファイルを送信する。
    """
    image_path = os.path.join("static", "images", user_id, photobook_name, filename)
    return send_file(image_path, mimetype='image/jpeg')

@app.teardown_appcontext
def shutdown_session(exception=None):
    """
    アプリケーションコンテキストが終了したときにデータベースセッションを閉じる。
    """
    db_session.remove()
