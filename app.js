function fetchInstagramPhotos() {
    const ACCESS_TOKEN = document.getElementById("token").value;

    if (!ACCESS_TOKEN) {
        alert("Please enter your ACCESS_TOKEN.");
        return;
    }

    const endpoint = `https://graph.instagram.com/1349872215956516/media?fields=id,caption&access_token=${ACCESS_TOKEN}`;

    fetch(endpoint)
        .then(response => response.json())
        .then(data => {
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
