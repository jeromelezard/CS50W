

document.addEventListener('DOMContentLoaded', () => {


    const textarea = document.querySelector('.postContent');
    textarea.addEventListener('input', function() {
        textarea.style.height = "50px";
        var scroll_height = textarea.scrollHeight;
        textarea.style.height = scroll_height+"px";

    })

    
    
});


function likePost(id) {
    fetch(`/like`, {
        method: 'POST',
        body: JSON.stringify({
            post_id: id,
        })
    })
    .then(response => response.json())
    .then(result => {
        console.log(result);
        if (result["error"] == 1) {
            document.getElementById(`${id}_likes`).innerHTML = 'Sign in to like';
            return false;
        }
        post = document.getElementById(id);
        if (post.classList.value == 'like') {
            post.classList.remove('like');
            post.classList.add('unlike');
        } else {
            post.classList.remove('unlike');
            post.classList.add('like');

        }
        if (result["likes"] == 0) {
            document.getElementById(`${id}_likes`).innerHTML = '';
        } else {
            document.getElementById(`${id}_likes`).innerHTML = result["likes"];
        }
    })
    .catch((error) => {
        console.log(error);
    });
}


function editButton(id) {
    
    document.getElementById(`${id}_edit`).classList.remove('hidden');
}
function editButtonLeave(id) {
    document.getElementById(`${id}_edit`).classList.add('hidden');

}
function editPost(post) {
    post.parentElement.children[3].style.display = 'block';
    post.parentElement.children[4].style.display = 'none';
    return false;
    
}
function saveEdit(post) {
    let new_post = post.parentElement.children[0].value;
    let post_id = post.parentElement.children[0].dataset.id;
    
    fetch('/saveEdit', {
        method: "POST",
        body: JSON.stringify({
            new_post: new_post,
            post_id: post_id,
        })

    })
    .then(response => response.json())
    .then(result => {
        console.log(result);
        post.parentElement.style.display = 'none';
        
        post.parentElement.parentElement.children[4].innerHTML = result["new_content"];

        post.parentElement.parentElement.children[4].style.display = 'block';
    });
}

const follow = document.getElementById('followButton');
follow.addEventListener('click', function() {
    fetch('/follow', {
        method: "POST",
        body: JSON.stringify({
            user: window.location.pathname.substring(window.location.pathname.lastIndexOf('/') + 1),
        })
    })
    .then(response => response.json())
    .then(result => {
        console.log(result);
        follow.innerHTML = result["message"];
        document.getElementById('followerCount').innerHTML = `${result["count"]} `;
    })
    .catch(error => {
        console.log(error);
    })
})

