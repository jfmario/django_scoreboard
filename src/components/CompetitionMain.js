
import React, { Component } from 'react';
import  { Link } from 'react-router-dom';

import moment from 'moment';

import WelcomeCompetition from './WelcomeCompetition';

/**
Component CompetitionMain
props: competitionId, competition
*/
class CompetitionMain extends Component {

  constructor(props) {

    super(props);

    this.state = {
      competition: null,
      competitionId: 0
    };
  }

  componentWillReceiveProps(props) {
    console.log(props);
    this.setState({
      competition: props.competition,
      competitionId: props.competitionId
    });
  }

  render() {
    return (
      <div>
        {!!(this.state.competition) &&
          <div>
            <WelcomeCompetition competitionId={this.state.competition.id} competition={this.state.competition} />
          </div>
        }
      </div>
    )
  }
}

export default CompetitionMain;
