document.addEventListener('DOMContentLoaded', () => {

    console.log('----');
    console.log('window.innerHeight');
    console.log('window.innerWidth');
    console.log('window.scrollY');
    console.log('document.body.offsetHeight');

    const height = window.innerHeight;
    document.querySelector('#page').style.height = height;
    document.querySelector('#page').style.width = width;
})

document.addEventListener('DOMContentLoaded', () => {
    document.querySelector('#create').disabled = true;
    document.querySelector('#channel').onkeyup = () => {
        if (document.querySelector('#channel').value.length > 0) 
            document.querySelector('#create').disabled = false;
        else
            document.querySelector('#create').disabled = true;
    
        };

    document.querySelector('#send').disabled = true;
    document.querySelector('#message').onkeyup = () => {
        if (document.querySelector('#message').value.length > 0) 
            document.querySelector('#send').disabled = false;
        else
            document.querySelector('#send').disabled = true;
    
        };

    });

document.addEventListener('DOMContentLoaded', () => {
    const user = document.querySelector('#user').innerHTML;
    
    var socket = io.connect(location.protocol + '//' + document.domain + ':' + location.port);
    socket.on('connect', () => {
        document.querySelector('#form1').onsubmit = () => {
            const message = document.querySelector('#message').value;
            socket.emit('message sent', {'message': message});
            document.querySelector('#message').value = '';
            document.querySelector('#send').disabled = true;

            return false;
        };

    });
    socket.on('message bc', data => {
        const div = document.createElement('div');
        div.className = 'alert alert-danger';
        div.style.height = "auto";

        const div1 = document.createElement('div');
        div1.style.color = "black";
        div1.innerHTML = `${data.message}`;
        div.append(div1);

        const span = document.createElement('div');
        span.className = 'user';
        span.style.fontSize = '10px'
        var today = new Date();
        var time = today.getHours() + ":" + today.getMinutes() + ":" + today.getSeconds();
        span.innerHTML = `- ${user} ${time}`;
        span.style.color = "grey";
        div.append(span);

        const hide = document.createElement('button');
        hide.className = 'delete';
        hide.innerHTML = 'Delete';
        div.append(hide);

        hide.onclick = function() {
            this.parentElement.remove();
        };

        document.querySelector('#message-area').append(div);
    });
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
        li.href = '#';
        li.style.borderStyle = "double";
        li.innerHTML = `${data.selection} channel`;
        document.querySelector('#channelslink').append(li);
        const br = document.createElement('br');
        document.querySelector('#channelslink').append(br);
    });
});


document.addEventListener('DOMContentLoaded', () => {
    document.querySelector('#create').onclick = () => {
        const alert = document.createElement('div');
        const channel = document.querySelector('#channel').value;
        alert.innerHTML = `${channel} succesfully created`;
        alert.className = 'alert alert-success'
        document.querySelector('#alert').append(alert);
    };
});

