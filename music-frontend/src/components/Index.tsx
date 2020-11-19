import React, { useContext } from 'react';
import UserContext from './UserContext';

export function Index() {

    const {user} = useContext(UserContext);

    return (
        <div>
            <h2>Index</h2>
            <div>{user}</div>
        </div>
    )
}

export default Index;