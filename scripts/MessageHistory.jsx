import * as React from 'react';
import { Socket } from './Socket';

export function MessageHistory() {
    const [messages, setMessages] = React.useState([]);
    
    function getMessages() {
        React.useEffect(() => {
            Socket.on('Chat history received', (data) => {
                console.log("Received Chat history from server: " + data['chatHistory']);
                setMessages(data['chatHistory']);
            })
        });
    }
    
    getMessages();
    
    return (
        <div id="messageHistory">
            <ul>
                {messages.map((message, index) =>
                    <li key={index} class={message['class']}>{message['sender']}: {message['message']}</li>)}
            </ul>
        </div>
    )
}
