import React, { useState } from 'react';
import './App.css';
import { BrowserRouter as Router, Route, Link } from 'react-router-dom';
import { AppBar, Tabs, Tab } from '@material-ui/core';

import { HorizOptionButton } from './components/MainOptions';
import { UserContext } from './components/UserContext';

import { Index } from './components/Index'
import { LoginUser } from './components/LoginUser'
import { CreateUser } from './components/CreateUser'

interface UserProps {
  user: string,
}

class App extends React.Component<UserProps, {user: ""}> {
  render() {
    return (
      <div className="App">
        <header className="App-header">
          <Router>
            <AppBar>
              <Tabs>
                <Link to='/' style={{ textDecoration: 'none' }}>
                  <Tab label="Home"/>
                </Link>
              </Tabs>
            </AppBar>
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
              
              <UserContext.Provider value={{user: this.props.user, changeUser: ()=> {}}}>
                <Route path="/" exact component = { Index }/>
                <Route path="/login/" component = { LoginUser }/>
                <Route path="/create/" component = { CreateUser }/>
              </UserContext.Provider>
          </Router>
        </header>
      </div>
    );
  }
}

export default App;
