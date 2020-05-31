document.addEventListener('DOMContentLoaded', () => {
    document.querySelector('#create').disabled = true;
    document.querySelector('#channel').onkeyup = () => {
        if (document.querySelector('#channel').value.length > 0) 
            document.querySelector('#create').disabled = false;
        else
            document.querySelector('#create').disabled = true;
    
        };
    

    });

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
        li.className = "container"
        li.href = document.querySelector('#channel').value;
        li.style.borderStyle = "double";
        li.innerHTML = `Channel ${data.selection}`;
        document.querySelector('#channelslink').append(li);
        const br = document.createElement('br');
        document.querySelector('#channelslink').append(br);
    });
});

document.addEventListener('DOMContentLoaded', () => {
    document.querySelector('#create').onclick = () => {
        const alrt = document.createElement('div');
        const channel = document.querySelector('#channel').value;
        alrt.innerHTML = `${channel} succesfully created`;
        alrt.className = 'alert alert-success'
        document.querySelector('#alrt').append(alrt);
    };
});

