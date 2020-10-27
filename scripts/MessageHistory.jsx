import * as React from 'react';
import Socket from './Socket';

function MessageHistory() {
  const [messages, setMessages] = React.useState([]);
  const [loggedIn, setLoginState] = React.useState(false);

  function setup() {
    React.useEffect(() => {
      Socket.on('Chat history received', (data) => {
        setMessages(data.chatHistory);
      });
    });

    React.useEffect(() => {
      Socket.on('login accepted', () => {
        setLoginState(true);
      });
    });
  }

  function createMessageHTML(senderPicUrl, messageHTML) {
    const HTMLstr = `<img src="${senderPicUrl}" class="profileImage" />${messageHTML}`;
    return { __html: HTMLstr };
  }

  setup();

  return (
    <div id="messageHistory">
      {loggedIn
        ? (
          <ul>
            {messages.map((message, index) => <li key={index} className={message.class} dangerouslySetInnerHTML={createMessageHTML(message.senderPic, message.message)} />)}
          </ul>
        )
        : <div id="obscuredMessageHistory" />}
    </div>
  );
}

export default MessageHistory;
