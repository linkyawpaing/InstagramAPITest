// Instagramの写真を取得する関数
function fetchInstagramPhotos() {
    // アクセストークンを取得
    const ACCESS_TOKEN = document.getElementById("token").value;
    // ユーザーIDを取得
    const USER_ID = document.getElementById("userId").value;

    // アクセストークンまたはユーザーIDがない場合は警告を表示
    if (!ACCESS_TOKEN || !USER_ID) {
        alert("Please enter your User ID and ACCESS_TOKEN.");
        return;
    }

    // Instagram APIのエンドポイントURLを構築
    const endpoint = `https://graph.facebook.com/v18.0/${USER_ID}/media?fields=id,caption,media_type,media_url&access_token=${ACCESS_TOKEN}`;

    // APIにリクエストを送信
    fetch(endpoint)
        .then(response => response.json())
        .then(data => {
            // エラーがある場合は例外を投げる
            if (data.error) {
                throw new Error(data.error.message);
            }
            // 写真を表示する
            displayPhotos(data.data);
        })
        .catch(error => {
            // エラーが発生した場合はコンソールにエラーを表示し、警告を表示
            console.error('Error fetching Instagram photos:', error);
            alert("An error occurred. Please check the console for more details.");
        });
}

// 写真を表示する関数
function displayPhotos(photos) {
    // 写真を表示するためのdiv要素を取得
    const photosDiv = document.getElementById("photos");
    // 以前の写真をクリア
    photosDiv.innerHTML = '';

    // 取得した写真を一つずつ処理
    photos.forEach(photo => {
        // 写真が画像の場合のみ処理
        if (photo.media_type === "IMAGE") {
            // img要素を作成し、写真のURLを設定
            const img = document.createElement('img');
            img.src = photo.media_url;
            img.alt = photo.caption ? photo.caption : 'Instagram Photo';
            img.width = 200;
            // img要素をdiv要素に追加
            photosDiv.appendChild(img);
        }
    });
}
