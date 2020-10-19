import * as React from 'react';
import { Socket } from './Socket';
import { GoogleButton } from './GoogleButton';

export function Button() {
    
    const [loggedIn, setLoginState] = React.useState(false);
    const [senderID, setSenderID] = React.useState(0)

    function setup() {
        React.useEffect(() => {
            Socket.on('login accepted', (data) => {
                setSenderID(data['senderKey']);
                setLoginState(true);
                console.log("Server acknowledged login")
            })
        });
    }

    function handleSubmit(event) {
        let newMessage = document.getElementById("message_input");
        Socket.emit('new message', {
            'msg': newMessage.value,
            'sender': senderID,
        });
        
        console.log('Sent the message ' + newMessage.value + ' from registered user number ' + senderID + ' to server!');
        newMessage.value = ''
        
        event.preventDefault();
    }

    setup();
    
    return (
        <div id="messageSubmission">
        {loggedIn ? 
            <form onSubmit={handleSubmit}>
                <input id="message_input" placeholder="Enter chat message here"></input>
                <button id="send_button">Send Message</button>
            </form>
        :
            <GoogleButton />
        }
        </div>
    )
}
