
import React, { Component } from 'react';
import  { Route, Switch } from 'react-router-dom';

import axios from 'axios';

import CompetitionHeader from '../components/CompetitionHeader';
import CompetitionMain from '../components/CompetitionMain';

class Competition extends Component {

  constructor(props) {

    super(props);

    this.state = {
      challengeGroups: [],
      competition: null,
      competitionId: props.match.params.competitionId,
      siteBranding: "Scoreboard",
      status: null,
      username: ''
    };
  }

  async componentDidMount() {

    this.loadCompetition(this.state.competitionId);

    var res = await axios.post(`/api/settings`);
    this.setState({
      siteBranding: res.data.siteBranding,
      username: res.data.username
    });
  }
  async componentWillReceiveProps(props) {
    if (props.match.params.competitionId != this.state.competitionId) {
      var competitionId = props.match.params.competitionId;
      await this.loadCompetition(competitionId);
      this.setState({
        competitionId: competitionId
      });
    }
  }
  async loadCompetition(competitionId) {
    var res = await axios.post(`/api/competitions/register/${competitionId}`);
    if (res.data.success) {

      res = await axios.post(`/api/competition/${competitionId}`);

      var challengeGroups = [];

      if (res.data.challenges)
        challengeGroups = res.data.challenges;

      this.setState({
        challengeGroups: challengeGroups,
        competition: res.data.competition,
        status: res.data.status
      });
    }
  }
  render() {

    var self = this;

    return (
      <div>
        <CompetitionHeader competitionId={this.state.competitionId} siteBranding={this.state.siteBranding} username={this.state.username} />

        <Switch>
          <Route exact path='/competition/:competitionId' render={(routeProps) => { return <CompetitionMain competitionId={routeProps.competitionId} competition={self.state.competition} challenges={self.state.challenges} /> }}/>
          <Route exact path='/competition/:competitionId/challenges' render={(routeProps) => { return <p>Challenges</p> }} />
          <Route exact path='/competition/:competitionId/leaderboard' render={(routeProps) => { return <p>Leaderboard</p> }} />
        </Switch>
      </div>
    )
  }
}

export default Competition;
