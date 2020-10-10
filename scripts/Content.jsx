    
import * as React from 'react';


import { Button } from './Button';
import { Socket } from './Socket';

export function Content() {
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
        <div>
            <div id="messageSubmission">
                <Button />
            </div>
            <div id="messageHistory">
                <ul>
                    {messages.map((message, index) =>
                        <li key={index}>{message}</li>)}
                </ul>
            </div>
        </div>
    );
}
