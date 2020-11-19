import { createContext, Dispatch, ReducerAction } from 'react';
import { IUser } from '../interfaces/IUser'

let context: IUser = {
    user: "",
    isLoggedIn: false,
    dispatch: (A: any): void => { }
}

export const UserContext = createContext<IUser>(context);