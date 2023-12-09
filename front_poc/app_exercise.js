// Instagramの写真を取得する関数
function fetchInstagramPhotos() {
    // アクセストークンを取得
    const ACCESS_TOKEN = document.getElementById("token").value;
    // ユーザーIDを取得
    const USER_ID = document.getElementById("userId").value;

    // TODO: アクセストークンまたはユーザーIDがない場合は警告を表示するコードを書く
    // ヒント: if文を使用して、ACCESS_TOKEN または USER_ID が空かどうかをチェックし、
    // 空の場合は alert 関数で警告メッセージを表示する

    // Instagram APIのエンドポイントURLを構築
    const endpoint = `https://graph.facebook.com/v18.0/${USER_ID}/media?fields=id,caption,media_type,media_url&access_token=${ACCESS_TOKEN}`;

    // APIにリクエストを送信
    fetch(endpoint)
        .then(response => response.json())
        .then(data => {
            // TODO: 写真を表示するための displayPhotos 関数を呼び出すコードを書く
            // ヒント: displayPhotos 関数に data.data を引数として渡す
        })
        .catch(error => {
            console.error('Error fetching Instagram photos:', error);
            alert("An error occurred. Please check the console for more details.");
        });
}

// 写真を表示する関数
function displayPhotos(photos) {
    // 写真を表示するためのdiv要素を取得
    const photosDiv = document.getElementById("photos");

    // TODO: photosDivのinnerHTMLを空にするコードを書く
    // ヒント: photosDivのinnerHTMLプロパティに空文字列を代入する

    // 取得した写真を一つずつ処理
    photos.forEach(photo => {
        // TODO: img要素を作成し、写真のURLを設定するコードを書く
        // ヒント: document.createElement 関数を使用して img 要素を作成し、
        // src 属性に photo.media_url を設定する
    });
}
