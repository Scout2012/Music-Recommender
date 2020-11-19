import React, { useContext } from 'react';
import { Redirect } from 'react-router';
import { UserContext } from './UserContext';


export const LogoutUser = () => {
  const {user, isLoggedIn, dispatch} = useContext(UserContext);
  if(isLoggedIn && user !== "") {
    localStorage.removeItem('session');
    dispatch({type: 'logout'}); //verificationResponse.body.username
  } else {
    console.log("AHHHHHHHHHH");
  }

  return (
    <Redirect to='/'/>
  );
}
