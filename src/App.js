
import React, { Component } from 'react';
import { render } from 'react-dom';
import { HashRouter } from 'react-router-dom';

import Main from './Main';

class App extends Component {
  render() {
    return (
      <HashRouter>
        <Main />
      </HashRouter>
    )
  }
}

render(<App />, document.getElementById('root'));
