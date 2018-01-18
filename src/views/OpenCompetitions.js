
import React, { Component } from 'react';
import  { Route, Switch } from 'react-router-dom';

import axios from 'axios';

import CompetitionCard from '../components/CompetitionCard';

class OpenCompetitions extends Component {

  constructor(props) {

    super(props);
    this.state = {
      competitions: []
    };
  }

  componentDidMount() {
    this.initialize();
  }
  componentWillReceiveProps(props){
    this.initialize(props);
  }

  async initialize(props) {
    var res = await axios.post('/api/competitions');
    console.log(res);
    this.setState({ competitions: res.data });
    console.log(this.state);
  }

  render() {
    return (
      <div className="container">

        <h2>Available Competitions</h2>

        <p>
          <i>A list of of competitions you are in or are eligible to join.</i>
        </p>

        <div className="columns">
          {this.state.competitions.map((c) => (
            <div className="column col-4">
              <CompetitionCard competition={c} />
           </div>
          ))}
        </div>
      </div>
    )
  }
}

export default OpenCompetitions;
