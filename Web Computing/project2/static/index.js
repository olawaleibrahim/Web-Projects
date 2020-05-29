document.addEventListener('DOMContentLoaded', () => {
    var socket = io.connect(location.protocol + '//' + document.domain + ':' + location.port);
    socket.on('connect', () => {
        document.querySelector('#form').onsubmit = () => {
            const selection = document.querySelector('#channel').value;
            socket.emit('create channel', {'selection': selection});
            document.querySelector('#channel').value = '';
            document.querySelector('#create').disabled = true;

            return false;
        };
    });

    socket.on('channel created', data => {
        const li = document.createElement('a');
        li.href = document.querySelector('#channel').value;
        li.innerHTML = `Channel ${data.selection}`;
        document.querySelector('#channelslink').append(li);
        const br = document.createElement('br');
        document.querySelector('#channelslink').append(br);
    });
});