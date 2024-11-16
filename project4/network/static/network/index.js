document.addEventListener('DOMContentLoaded', function() {
    document.querySelectorAll('.edit-page').forEach(editPage => {
        editPage.style.display = "none";
    });
    
    document.querySelectorAll(".close-button").forEach((button, index) => {
        button.addEventListener('click', (event) => {
            const postId = button.dataset.postId;
            hidePage(event, postId);
        });
    });

    document.querySelectorAll(".edit-button").forEach((button, index) => {
        button.addEventListener('click', (event) => {
            event.preventDefault();
            const postId = button.dataset.postId;
            //console.log("Editar ID:", postId);   
            document.getElementById(`edit-page-${postId}`).style.display = "block";       
            document.getElementById(`cointainer-text-${postId}`).style.display = "none";    
        });
    });

    document.querySelectorAll(".save-button").forEach((button, index) => {
        button.addEventListener('click', (event) => {
            const postId = button.dataset.postId;
            //console.log(postId)
            saveComment(postId);
            hidePage(event, postId);
        });
    });

    document.querySelectorAll(".liked-button").forEach((button) => {
        button.addEventListener('click', (event) => {
            const postId = button.dataset.postId;
            likePost(event, postId).then(data => {
                document.querySelector(`#likes-count-${postId}`).textContent = data.likes_count;

                button.classList.remove("liked-button");
                button.classList.add("unliked-button");
                button.innerHTML = `
                    <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="red" class="bi bi-heart-fill" viewBox="0 0 16 16">
                        <path fill-rule="evenodd" d="M8 1.314C12.438-3.248 23.534 4.735 8 15-7.534 4.736 3.562-3.248 8 1.314"/>
                    </svg>
                `;
            });
        });
    });

    document.querySelectorAll(".unliked-button").forEach((button) => {
        button.addEventListener('click', (event) => {
            const postId = button.dataset.postId;
            unlikePost(event, postId).then(data => {
                console.log(data.likes_count);
                document.querySelector(`#likes-count-${postId}`).textContent = data.likes_count;

                button.classList.remove("unliked-button");
                button.classList.add("liked-button");
                button.innerHTML = `
                    <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-heart" viewBox="0 0 16 16">
                        <path d="m8 2.748-.717-.737C5.6.281 2.514.878 1.4 3.053c-.523 1.023-.641 2.5.314 4.385.92 1.815 2.834 3.989 6.286 6.357 3.452-2.368 5.365-4.542 6.286-6.357.955-1.886.838-3.362.314-4.385C13.486.878 10.4.28 8.717 2.01zM8 15C-7.333 4.868 3.279-3.04 7.824 1.143q.09.083.176.171a3 3 0 0 1 .176-.17C12.72-3.042 23.333 4.867 8 15"/>
                    </svg>
                `;
            });
        });
    });
});


function hidePage(event, postId) {
    event.preventDefault();
    //console.log("close");
    document.getElementById(`edit-page-${postId}`).style.display = "none";
    document.getElementById(`cointainer-text-${postId}`).style.display = "block";
    //console.log(postId);
}

function getCookie(name) {
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    if (parts.length === 2) return parts.pop().split(';').shift();
}

function saveComment(postId) {  
    const new_text = document.getElementById(`edited-text-${postId}`).value;

    console.log(JSON.stringify({ text: new_text }));
    console.log('CSRF Token:', getCookie('csrftoken'));

    fetch(`/edit_post/${postId}/`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken')
        },
        body: JSON.stringify({ 
            text: new_text, 
        }),
    })
    .then(response => response.json())
    .then(result => {
        console.log(result);
        document.getElementById(`text-post-${postId}`).innerText = new_text;
    })
}

function likePost(event, postId) {
    console.log("CUrti")
    console.log(postId)

    return fetch(`/like_post/${postId}`)
    .then(response => response.json())
    .then(result => {
        console.log(result);
        return result;
    })    
}


function unlikePost(event, postId) {
    console.log("Descurti")
    console.log(postId)

    return fetch(`/unlike_post/${postId}`)
    .then(response => response.json())
    .then(result => {
        console.log(result);
        return result;
    })
}
