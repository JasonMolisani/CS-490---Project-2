import * as React from 'react';
import { Socket } from './Socket';
import escape from 'underscore/modules/escape.js';

export function MessageHistory() {
    const [messages, setMessages] = React.useState([]);
    const [loggedIn, setLoginState] = React.useState(false)
    
    function setup() {
        React.useEffect(() => {
            Socket.on('Chat history received', (data) => {
                console.log("Received Chat history from server: " + data['chatHistory']);
                setMessages(data['chatHistory']);
            })
        });
        
        React.useEffect(() => {
            Socket.on('login accepted', (data) => {
                setLoginState(true);
                console.log("MessageHistory saw server acknowledging login")
            })
        });
    }
    
    function createMessageHTML(senderPicUrl, messageHTML) {
        let HTMLstr = '<img src="' + senderPicUrl + '" class="profileImage" />' + messageHTML;
        return {__html: HTMLstr};
    }
    
    setup();
    
    return (
        <div id="messageHistory">
            {loggedIn ?
                <ul>
                    {messages.map((message, index) =>
                        <li key={index} className={message['class']} dangerouslySetInnerHTML={createMessageHTML(message['senderPic'], message['message'])} ></li>)}
                </ul>
            :
                <div id="obscuredMessageHistory">
                </div>
            }
        </div>
    )
}
