
import React, { Component } from 'react';
import  { Route, Switch } from 'react-router-dom';

import Competition from './views/Competition';
import OpenCompetitions from './views/OpenCompetitions';

class Main extends Component {

  constructor(props) {

    super(props);
  }

  async componentDidMount() {
  }

  render() {
    return (
      <div className="container">
        <div className="columns">
          <div className="col-8 col-mx-auto">
            <Switch>
              <Route exact path="/" component={OpenCompetitions} />
              <Route path="/competition/:competitionId" component={Competition} />
            </Switch>
          </div>
        </div>
      </div>
    )
  }
}

export default Main;
