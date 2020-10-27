import * as React from 'react';

import MessageHistory from './MessageHistory';
import Button from './Button';
import Socket from './Socket';

function Content() {
  const [numUsers, setNumUsers] = React.useState([]);

  function updateNumUsers() {
    React.useEffect(() => {
      Socket.on('someone connected', (data) => {
        setNumUsers(data.numUsers);
      });
    });

    React.useEffect(() => {
      Socket.on('someone disconnected', (data) => {
        setNumUsers(data.numUsers);
      });
    });

    React.useEffect(() => {
      Socket.on('someone logged in', (data) => {
        setNumUsers(data.numUsers);
      });
    });
  }
  updateNumUsers();

  return (
    <div>
      <div id="chatRoomStats">
        <p>
          Number of users in chat room:
          {numUsers}
        </p>
      </div>
      <MessageHistory />
      <Button />
    </div>
  );
}

export default Content;
