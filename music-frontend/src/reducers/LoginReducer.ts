import { ILoginReducer } from "../interfaces/ILoginReducer";

export const LoginReducer = (state: any, action: any) => {
    switch (action.type) {
        case 'login':
            return {
                ...state,
                user: "jacob",
                isLoggedIn: true,
            }
        default:
            break;
    }
}