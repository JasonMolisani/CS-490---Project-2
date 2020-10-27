import * as React from 'react';
import Socket from './Socket';
import GoogleButton from './GoogleButton';

function Button() {
  const [loggedIn, setLoginState] = React.useState(false);
  const [senderID, setSenderID] = React.useState(0);

  function setup() {
    React.useEffect(() => {
      Socket.on('login accepted', (data) => {
        setSenderID(data.senderKey);
        setLoginState(true);
      });
    });
  }

  function handleSubmit(event) {
    const newMessage = document.getElementById('message_input');
    Socket.emit('new message', {
      msg: newMessage.value,
      sender: senderID,
    });

    newMessage.value = '';

    event.preventDefault();
  }

  setup();

  return (
    <div id="messageSubmission">
      {loggedIn
        ? (
          <form onSubmit={handleSubmit}>
            <input id="message_input" placeholder="Enter chat message here" />
            <button id="send_button" type="submit">Send Message</button>
          </form>
        )
        : <GoogleButton />}
    </div>
  );
}

export default Button;
