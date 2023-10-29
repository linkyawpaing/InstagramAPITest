# ベースイメージの指定
# FROM python:3.12.0-slim-bookworm
FROM python:3.10.8-bullseye

# 作業ディレクトリの設定
WORKDIR /app

# 依存関係のインストール
RUN apt-get update && \
    apt-get install -y \
        default-libmysqlclient-dev \
        gcc \
        pkg-config \
        python3-dev \
        build-essential && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# requirements.txtのコピーとPython依存関係のインストール
COPY requirements.txt .
RUN pip install --no-cache -r requirements.txt

# アプリケーションのコードをコピー
COPY . .

# コンテナ起動時のコマンド
CMD ["uwsgi", "--ini", "app.ini"]
