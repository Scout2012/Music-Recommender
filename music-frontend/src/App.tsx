import React, { FunctionComponent, useEffect, useReducer } from 'react';
import './App.css';
import { BrowserRouter as Router, Route, Link, Redirect } from 'react-router-dom';
import { AppBar, Tabs, Tab } from '@material-ui/core';

import { LoginReducer } from './reducers/LoginReducer'

import { UserContext } from './components/UserContext';
import { Index } from './components/Index'
import { LoginUser } from './components/LoginUser'
import { LogoutUser } from './components/LogoutUser'
import { CreateUser } from './components/CreateUser'
import { UserProfile } from './components/UserProfile'

let buttonStyle = {
  textDecoration: 'none',
  color: 'white',
}

const App: FunctionComponent<{}> = () => {

  // const [username, setUser] = useState(user);
  const [{user, isLoggedIn}, dispatch] = useReducer(LoginReducer, {user: "", isLoggedIn: false})
  let session = localStorage.getItem('session');
  let navBar;
  console.log(session)
  
  useEffect(() => {
    if(session !== undefined && session != null) {
      console.log(session)
      console.log(true)
      dispatch({type: 'login', payload: session})
    } else {
      dispatch({type: 'logout'})
    }
  }, []);

  if(user !== "") { 
    navBar = [
      <Link to='/' style={buttonStyle}>
        <Tab label="Home"/>
      </Link>,
      <Link to='/logout/' style={buttonStyle}>
        <Tab label="Logout"/>
      </Link>,
      <Link to={`/users/${user}`}>
        <Tab label={user}/>
      </Link>
    ]
  } else {
    navBar = [
      <Link to='/' style={buttonStyle}>
        <Tab label="Home"/>
      </Link>,
    ]
  }

  return (
    <div className="App">
      <header className="App-header">
        <Router>
          <AppBar>
            <Tabs>
              {navBar}
            </Tabs>
          </AppBar>
          <UserContext.Provider value={{user, isLoggedIn, dispatch}}>
            <Route path="/" exact component = { Index }/> 
            <Route path="/login/" component = { LoginUser }>{isLoggedIn ? <Redirect to='/'/>: <LoginUser/>}</Route>
            <Route path="/logout/" component = { LogoutUser }/>
            <Route path="/create/" component = { CreateUser }/>
            <Route path="/users/:user" component = { UserProfile }/>
          </UserContext.Provider>
        </Router>
      </header>
    </div>
  );
}

export default App;
