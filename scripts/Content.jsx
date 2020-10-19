    
import * as React from 'react';


import { Button } from './Button';
import { Socket } from './Socket';

export function Content() {
    const [messages, setMessages] = React.useState([]);
    const [numUsers, setNumUsers] = React.useState([]);
    
    function getMessages() {
        React.useEffect(() => {
            Socket.on('Chat history received', (data) => {
                console.log("Received Chat history from server: " + data['chatHistory']);
                setMessages(data['chatHistory']);
            })
        });
    }
    
    function updateNumUsers() {
        React.useEffect(() => {
            Socket.on('someone connected', (data) => {
                setNumUsers(data['numUsers']);
            })
        });
        
        
        React.useEffect(() => {
            Socket.on('someone disconnected', (data) => {
                setNumUsers(data['numUsers']);
            })
        });
    }
    
    getMessages();
    updateNumUsers();

    return (
        <div>
            <div id="chatRoomStats">
                <p>Number of users in chat room: {numUsers}</p>
            </div>
            <div id="messageHistory">
                <ul>
                    {messages.map((message, index) =>
                        <li key={index} class={message['class']}>{message['sender']}: {message['message']}</li>)}
                </ul>
            </div>
            <Button />
        </div>
    );
}
