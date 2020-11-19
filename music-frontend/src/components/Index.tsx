import React, { FunctionComponent, useContext } from 'react';
import { Button } from '@material-ui/core';
import { IUser } from '../interfaces/IUser';
import HorizOptionButton from './MainOptions';
import { UserContext } from './UserContext';

export const Index : FunctionComponent<IUser> = () => {
    const {user, isLoggedIn, dispatch} = useContext(UserContext);

    let mainContent;
    let buttons;

    if(!isLoggedIn) {
        buttons = <HorizOptionButton options={[
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
    }

    return (
        <div>
            <h2>Index</h2>
            {buttons}
            {mainContent}
        </div>
    )
}

export default Index;