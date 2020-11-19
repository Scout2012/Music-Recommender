import React, { FunctionComponent, useReducer, useState } from 'react';
import './App.css';
import { BrowserRouter as Router, Route, Link } from 'react-router-dom';
import { AppBar, Tabs, Tab } from '@material-ui/core';

import { LoginReducer } from './reducers/LoginReducer'

import { UserContext } from './components/UserContext';
import { Index } from './components/Index'
import { LoginUser } from './components/LoginUser'
import { CreateUser } from './components/CreateUser'
import { IUser } from './interfaces/IUser';

let buttonStyle = {
  textDecoration: 'none',
  color: 'white',
}

const App: FunctionComponent<{}> = () => {

  // const [username, setUser] = useState(user);
  const [{user, isLoggedIn}, dispatch] = useReducer(LoginReducer, {user: "", isLoggedIn: false}) 
  let navBar;

  if(user !== "") { 
    navBar = [
      <Link to='/' style={buttonStyle}>
        <Tab label="Home"/>
      </Link>,
      <Link to='/logout/' style={buttonStyle}>
        <Tab label="Logout"/>
      </Link>,
      <Link to='/logout/' style={buttonStyle}>
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
            <Route path="/login/" component = { LoginUser }/>
            <Route path="/create/" component = { CreateUser }/>
          </UserContext.Provider>
        </Router>
      </header>
    </div>
  );
}

export default App;
