import * as React from 'react';
import { Socket } from './Socket';

function handleSubmit(event) {
    let newMessage = document.getElementById("message_input");
    let sender = document.getElementById("sender_input");
    Socket.emit('new item input', {
        'item': newMessage.value,
        'sender': sender.value,
    });
    
    console.log('Sent the grocery item ' + newMessage.value + ' to server!');
    newMessage.value = ''
    
    event.preventDefault();
}

export function Button() {
    return (
        <form onSubmit={handleSubmit}>
            <input id="sender_input" placeholder="Enter username here"></input>
            <input id="message_input" placeholder="Enter chat message here"></input>
            <button>Send Message</button>
        </form>
    );
}
