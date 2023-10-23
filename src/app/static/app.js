const $ = (selector) => document.querySelector(selector);

function getInputs() {
    return {
        ACCESS_TOKEN: $("#token").value,
        USER_ID: $("#userId").value,
        HASHTAG: $("#hashtag").value,
        PHOTOBOOK_NAME: $("#photobookName").value
    };
}

function handleError(error, message) {
    console.error(message, error);
    alert("An error occurred. Please check the console for more details.");
}

function fetchFromEndpoint(endpoint, options = {}) {
    return fetch(endpoint, options)
        .then(response => response.json())
        .then(data => {
            if (data.error) {
                throw new Error(data.error.message);
            }
            return data;
        });
}

function displayPhotos(photosData) {
    const photosDiv = $("#photos");
    photosDiv.innerHTML = '';

    photosData.forEach(photo => {
        if (photo.media_type === "IMAGE") {
            const img = document.createElement('img');
            img.src = photo.media_url;
            img.alt = photo.caption || 'Instagram Photo';
            img.width = 200;
            photosDiv.appendChild(img);
        }
    });
}

function displayLocalPhotos(data) {
    const photosDiv = $("#photos");
    photosDiv.innerHTML = '';

    data.photos.forEach(filename => {
        const img = document.createElement('img');
        img.src = `/get_image/${data.user_id}/${data.photobook_name}/${filename}`;
        img.alt = 'Instagram Photo';
        img.width = 200;
        photosDiv.appendChild(img);
    });
}

function displayHashtags(hashtags) {
    const hashtagsDiv = $("#hashtags");
    hashtagsDiv.innerHTML = '<h3>Your Hashtags:</h3>';

    hashtags.forEach(tag => {
        const p = document.createElement('p');
        p.textContent = `#${tag[0]}: ${tag[1]} times`;
        hashtagsDiv.appendChild(p);
    });
}

function fetchInstagramPhotos() {
    const { ACCESS_TOKEN, USER_ID } = getInputs();

    if (!ACCESS_TOKEN || !USER_ID) {
        alert("Please enter your User ID and ACCESS_TOKEN.");
        return;
    }

    const endpoint = `https://graph.facebook.com/v18.0/${USER_ID}/media?fields=id,caption,media_type,media_url&access_token=${ACCESS_TOKEN}`;

    fetchFromEndpoint(endpoint)
        .then(data => displayPhotos(data.data))
        .catch(error => handleError(error, 'Error fetching Instagram photos:'));
}

function fetchHashtags() {
    const { ACCESS_TOKEN, USER_ID } = getInputs();

    if (!ACCESS_TOKEN || !USER_ID) {
        alert("Please enter your User ID and ACCESS_TOKEN.");
        return;
    }

    const endpoint = `/fetch_hashtags`;

    fetchFromEndpoint(endpoint, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ userId: USER_ID, token: ACCESS_TOKEN })
    })
    .then(data => displayHashtags(data.hashtags))
    .catch(error => handleError(error, 'Error fetching hashtags:'));
}

function searchByHashtag() {
    const { ACCESS_TOKEN, USER_ID, HASHTAG } = getInputs();

    if (!ACCESS_TOKEN || !USER_ID || !HASHTAG) {
        alert("Please enter your User ID, ACCESS_TOKEN, and hashtag.");
        return;
    }

    const endpoint = `/search_by_hashtag`;

    fetchFromEndpoint(endpoint, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ userId: USER_ID, token: ACCESS_TOKEN, hashtag: HASHTAG })
    })
    .then(data => displayPhotos(data.photos))
    .catch(error => handleError(error, 'Error searching photos by hashtag:'));
}

function createPhotobook() {
    const { ACCESS_TOKEN, USER_ID, PHOTOBOOK_NAME } = getInputs();
    const photosDiv = $("#photos");
    const photos = Array.from(photosDiv.getElementsByTagName("img")).map(img => img.src);

    fetchFromEndpoint('/create_photobook', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ name: PHOTOBOOK_NAME, userId: USER_ID, photos: photos })
    })
    .then(data => alert(data.message))
    .catch(error => handleError(error, 'Error creating photobook:'));
}

function loadPhotobooks() {
    const { USER_ID } = getInputs();

    if (!USER_ID) {
        alert("Please enter your User ID.");
        return;
    }

    fetchFromEndpoint(`/get_photobooks?userId=${USER_ID}`)
    .then(data => {
        const photobookList = $("#photobookList");
        photobookList.innerHTML = '';

        data.photobooks.forEach(photobook => {
            const option = document.createElement('option');
            option.value = photobook;
            option.textContent = photobook;
            photobookList.appendChild(option);
        });
    })
    .catch(error => handleError(error, 'Error loading photobooks:'));
}

function displaySelectedPhotobook() {
    const { USER_ID } = getInputs();
    const selectedPhotobook = $("#photobookList").value;

    fetchFromEndpoint(`/get_photobook_photos`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ userId: USER_ID, photobookName: selectedPhotobook })
    })
    .then(data => displayLocalPhotos(data))
    .catch(error => handleError(error, 'Error displaying selected photobook:'));
}
