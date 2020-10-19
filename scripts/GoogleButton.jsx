import React from 'react';
import { Socket } from './Socket';
import ReactDOM from 'react-dom';
import GoogleLogin from 'react-google-login';

function handleSubmit(response) {
    console.log('successful login')
    console.log(response)
    
    let profilePic = response['profileObj']['imageUrl'];
    let email = response['profileObj']['email'];
    Socket.emit('new user login', {
        'email': email,
        'picUrl': profilePic,
    });
    
    console.log('Login associated with ' + email + ' sent to server!');
}

function handleFail(response) {
    console.log('login failed')
    console.log(response)
}

export function GoogleButton() {
    return (
            <GoogleLogin
                clientId="780345643535-79b302fg2hmq7u0r89mp0cch5rtr94ju.apps.googleusercontent.com"
                buttonText="Register"
                onSuccess={handleSubmit}
                onFailure={handleFail}
                cookiePolicy={'single_host_origin'}
            />
    );
}
