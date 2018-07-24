document.addEventListener('DOMContentLoaded', () => {

    // Connect to websocket
    var socket = io.connect(location.protocol + '//' + document.domain + ':' + location.port);

    // When connected, configure chatbox
    socket.on('connect', () => {

        //input box should spit messages
        document.querySelector('send', () => {
            send.onclick = () => {
              const message = send.dataset.message;
              socket.emit('send message', {'message': message})
            };
        });
    });

    // when new message is sent, add that to list
});
