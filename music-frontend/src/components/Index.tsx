import React, { FunctionComponent } from 'react';
import { IUser } from '../interfaces/IUser';
import HorizOptionButton from './MainOptions';

export const Index : FunctionComponent<IUser> = () => {

    return (
        <div>
            <h2>Index</h2>
            
            <HorizOptionButton options={[
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
        </div>
    )
}

export default Index;