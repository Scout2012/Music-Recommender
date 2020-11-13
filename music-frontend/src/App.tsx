import React from 'react';
import './App.css';
import { BrowserRouter as Router, Route, Link } from 'react-router-dom';
import { AppBar, Tabs, Tab } from '@material-ui/core';

import { HorizOptionButton } from './components/MainOptions'

function App() {
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
            
            <Route path="/"/>
            <Route path="/login/"/>
            <Route path="/create/"/>
        </Router>
      </header>
    </div>
  );
}

export default App;
