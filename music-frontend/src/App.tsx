import React from 'react';

import './App.css';
import Button from '@material-ui/core/Button';
import Grid from '@material-ui/core/Grid';

function App() {
  return (
    <div className="App">
      <header className="App-header">
        <Grid container spacing={2}>
          <Grid item xs={12}>
            <Grid container justify="center" spacing={2}>
                <Grid key={0} item>
                  <Button variant="contained" color="primary">
                    Login
                  </Button>
                </Grid>
                <Grid key={1} item>
                  <Button variant="contained" color="primary">
                    Create Account
                  </Button>
                </Grid>
            </Grid>
          </Grid>
        </Grid>
      </header>
    </div>
  );
}

export default App;
