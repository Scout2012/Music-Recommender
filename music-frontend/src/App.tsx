import React from 'react';
import './App.css';

import { HorizOptionButton } from './components/MainOptions'

function App() {
  return (
    <div className="App">
      <header className="App-header">
        <HorizOptionButton options={[
          {
            name: "Login",
            id: 0,
          },
          {
            name: "Create Account",
            id: 1,
          },
        ]}/>
      </header>
    </div>
  );
}

export default App;
