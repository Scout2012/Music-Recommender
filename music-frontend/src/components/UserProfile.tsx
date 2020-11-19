import React, { useContext } from 'react';
import { UserContext } from './UserContext';

export const UserProfile = () => {

    const {user, isLoggedIn, dispatch} = useContext(UserContext);

    return (
        <div> Hi, {user} </div>
    )
}