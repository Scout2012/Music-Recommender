import React, { FunctionComponent, useContext } from 'react';
import { Button } from '@material-ui/core';
import { IUser } from '../interfaces/IUser';
import HorizOptionButton from './MainOptions';
import { UserContext } from './UserContext';
import { UserProfile } from './UserProfile';

export const Index : FunctionComponent<IUser> = () => {
    const {user, isLoggedIn, dispatch} = useContext(UserContext);

    let mainContent;
    // let buttons;

    if(!isLoggedIn) {
        mainContent = <HorizOptionButton options={[
            {
                name: "Login",
                id: 0,
                route: "/login/",
            },
            {
                name: "Create Account",
                id: 1,
                route: "/create/",
            },
        ]}/>
    } else {
        // mainContent = User Profile Page
        mainContent = <h1>hi!</h1>
    }

    return (
        <div>
            {/* {buttons} */}
            {mainContent}
        </div>
    )
}

export default Index;