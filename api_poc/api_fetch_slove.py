import requests
from dotenv import load_dotenv
import os

# 環境変数の読み込み
load_dotenv()
INSTAGRAM_ACCESS_TOKEN = os.getenv('INSTAGRAM_ACCESS_TOKEN')

# ユーザープロフィールを取得する関数
def get_user_profile():
    url = f"https://graph.facebook.com/v18.0/me?fields=id%2Cname&access_token={INSTAGRAM_ACCESS_TOKEN}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception("API request failed with status code " + str(response.status_code))

# データを処理して表示する関数
def process_data(data):
    print(data)
    print("User ID:", data['id'])
    print("Username:", data['name'])

# エラーハンドリングを行う関数
def handle_errors(e):
    print("An error occurred:", e)

# メイン関数
def main():
    try:
        profile = get_user_profile()
        process_data(profile)
    except Exception as e:
        handle_errors(e)

if __name__ == "__main__":
    main()
