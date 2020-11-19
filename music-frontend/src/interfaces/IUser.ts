import { Dispatch, ReducerAction } from "react";

export interface IUser {
    user: string,
    isLoggedIn: boolean,
    dispatch: Dispatch<ReducerAction<any>>
}