import React from 'react';
import GoogleLogin from 'react-google-login';
import Socket from './Socket';

function handleSubmit(response) {
  const profilePic = response.profileObj.imageUrl;
  const { email } = response.profileObj;
  Socket.emit('new user login', {
    email,
    picUrl: profilePic,
  });
}

function GoogleButton() {
  return (
    <GoogleLogin
      clientId="780345643535-79b302fg2hmq7u0r89mp0cch5rtr94ju.apps.googleusercontent.com"
      buttonText="Register"
      onSuccess={handleSubmit}
      cookiePolicy="single_host_origin"
    />
  );
}

export default GoogleButton;
