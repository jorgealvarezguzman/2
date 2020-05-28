// Set starting value of counter to 0
if (!localStorage.getItem('displayName'))
    localStorage.setItem('displayName', '');

document.addEventListener('DOMContentLoaded', () => {
    // Load stored name
    document.querySelector('#nameHeader').innerHTML = localStorage.getItem('displayName');
    // Connect to websocket
    var socket = io.connect(location.protocol + '//' + document.domain + ':' + location.port);

    // When connected, configure buttons
    socket.on('connect', () => {

        document.querySelector('#form').onsubmit = () => {
            var displayName = document.querySelector('#displayName').value;

            socket.emit('submit displayName', {'displayName': displayName});

            return false;
        };

        document.querySelector('#channelForm').onsubmit = () => {
            const channel = document.querySelector('#channel').value;

            socket.emit('submit channel', {'channel': channel})

            return false;
        };

        document.querySelector('#post').onsubmit = () => {
            const post = document.querySelector("#post_text").value;

            socket.emit('submit post', {'post': post})

            return false;
        };

        // Set links up to load new pages.
        document.querySelectorAll('.nav-link').forEach(link => {
            link.onclick = () => {
                const page = link.dataset.page;
                load_page(page);
                return false;
            };
        });

    });

    socket.on('confirmDisplayName', displayName => {
        document.querySelector('#nameHeader').innerHTML = `${displayName}`;
        document.querySelector('#result').innerHTML = `Welcome ${displayName}!`;
        localStorage.setItem('displayName', `${displayName}`);
    });

    // When a channel is created, add to the unordered list
    socket.on('addChannel', channel => {
        const li = document.createElement('li');
        var channel_url = window.location.origin + `/channel/${channel}`;
        li.innerHTML =`<a href="${channel_url}" class="nav-link" data-page="${channel}">${channel}</a>`;
        document.querySelector('#channels').append(li);
    });

    // When a post is created, add it to the channel
    socket.on('addPost', post => {
        add_post(post);
    });

});

// Renders contents of new page in main view.
function load_page(name) {
    const request = new XMLHttpRequest();
    request.open('POST', `/channel/${name}`);
    request.onload = () => {
        const data = JSON.parse(request.responseText);
        //document.querySelector('#body').innerHTML = response;
        document.querySelector('#posts').innerHTML = `successfully displaying channel ${name}.`;
        data.forEach(add_post);
        // Push state to URL.
        document.title = name;
        history.pushState(null, name, name);
    };
    request.send();
}

// Add a new post
function add_post(contents) {
    // Create new post.
    const post = document.createElement('div');
    post.className = 'post';
    post.innerHTML = contents;

    // Add post to DOM.
    document.querySelector('#posts').append(post);
}
