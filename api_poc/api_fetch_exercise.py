import requests
from dotenv import load_dotenv
import os

# 環境変数の読み込み
load_dotenv()
INSTAGRAM_ACCESS_TOKEN = os.getenv('INSTAGRAM_ACCESS_TOKEN')

# ユーザープロフィールを取得する関数
def get_user_profile():
    # TODO: Instagram APIのURLを構築する
    # ヒント: f-stringを使用してINSTAGRAM_ACCESS_TOKENを読み出してURLを構築する
    url = f"https://graph.facebook.com/v18.0/me?fields=id%2Cname&access_token={}"

    # TODO: リクエストを送信し、レスポンスを取得する
    # ヒント: requests.getを使用してリクエストを送信し、response変数に格納する
    response = None

    # TODO: レスポンスが成功した場合はJSONデータを返す
    # ヒント: response.status_codeが200の場合、response.json()を返す
    if response:
        pass
    else:
        raise Exception("API request failed with status code " + str(response.status_code))

# メイン関数
def main():
    try:
        # TODO: get_user_profile関数を呼び出し、結果を表示する
        # ヒント: get_user_profile関数を呼び出し、その結果をprint関数で表示する
        profile = None
        print(profile)
    except Exception as e:
        print("An error occurred:", e)

if __name__ == "__main__":
    main()
