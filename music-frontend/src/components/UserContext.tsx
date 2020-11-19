import { createContext } from 'react';

export const UserContext = createContext({
    user: "",
    changeUser: () => {},
});

export default UserContext;