import * as React from 'react';
import { Socket } from './Socket';

function handleSubmit(event) {
    let newMessage = document.getElementById("message_input");
    let sender = document.getElementById("sender_input");
    Socket.emit('new message', {
        'msg': newMessage.value,
        'sender': sender.value,
    });
    
    console.log('Sent the message ' + newMessage.value + ' from ' + sender.value + ' to server!');
    newMessage.value = ''
    
    event.preventDefault();
}

export function Button() {
    
    function setup() {
        React.useEffect(() => {
            Socket.on('someone connected', (data) => {
                let sender = document.getElementById("sender_input");
                if (sender.value == "") {
                    console.log("Initialized username to : " + data['defaultUsername']);
                    sender.value = data['defaultUsername']
                }
            })
        });
    }

    setup()
    
    return (
        <form onSubmit={handleSubmit}>
            <input id="sender_input" placeholder="Enter username here"></input>
            <input id="message_input" placeholder="Enter chat message here"></input>
            <button id="send_button">Send Message</button>
        </form>
    );
}
