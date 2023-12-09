function fetchInstagramPhotos() {
    const ACCESS_TOKEN = document.getElementById("token").value;
    const USER_ID = document.getElementById("userId").value; // ユーザーIDを取得

    if (!ACCESS_TOKEN || !USER_ID) {
        alert("Please enter your User ID and ACCESS_TOKEN.");
        return;
    }

    const endpoint = `https://graph.facebook.com/v18.0/${USER_ID}/media?fields=id,caption,media_type,media_url&access_token=${ACCESS_TOKEN}`;

    fetch(endpoint)
        .then(response => response.json())
        .then(data => {
            if (data.error) {
                throw new Error(data.error.message);
            }
            displayPhotos(data.data);
        })
        .catch(error => {
            console.error('Error fetching Instagram photos:', error);
            alert("An error occurred. Please check the console for more details.");
        });
}

function displayPhotos(photos) {
    const photosDiv = document.getElementById("photos");
    photosDiv.innerHTML = ''; // Clear previous photos

    photos.forEach(photo => {
        if (photo.media_type === "IMAGE") {
            const img = document.createElement('img');
            img.src = photo.media_url;
            img.alt = photo.caption ? photo.caption : 'Instagram Photo';
            img.width = 200;
            photosDiv.appendChild(img);
        }
    });
}
