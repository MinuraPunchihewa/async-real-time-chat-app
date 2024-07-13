form = document.querySelector('#send-message');
form.addEventListener('submit', sendMessage);


function sendMessage(event) {
    event.preventDefault();
    
    const handle = document.querySelector('#handle').value;
    const message = document.querySelector('#message').value;

    const data = {
        handle,
        message,
    };

    socket.send(JSON.stringify(data));
    document.querySelector('#message').value = '';
    document.querySelector('#message').focus();
}