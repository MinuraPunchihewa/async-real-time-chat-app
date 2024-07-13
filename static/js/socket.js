const wsProtocol = window.location.protocol === 'https:' ? 'wss' : 'ws';
const wsUrl = `${wsProtocol}://${window.location.host}/ws`;

const socket = new WebSocket(wsUrl);

socket.onmessage = appendMessage;


function appendMessage(event) {
    console.log(event.data);

    const message = JSON.parse(event.data);

    const tr = document.createElement('tr');

    const handleTd = document.createElement('td');
    handleTd.appendChild(document.createTextNode(message.handle));

    const messageTd = document.createElement('td');
    messageTd.appendChild(document.createTextNode(message.message));

    tr.appendChild(handleTd);
    tr.appendChild(messageTd);

    const tbody = document.querySelector('#chat tbody');
    tbody.appendChild(tr);
}
