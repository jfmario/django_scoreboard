
import React, { Component } from 'react';
import  { Route, Switch } from 'react-router-dom';

import axios from 'axios';

import ChallengesMain from '../components/ChallengesMain';
import CompetitionHeader from '../components/CompetitionHeader';
import CompetitionMain from '../components/CompetitionMain';
import Leaderboard from '../components/Leaderboard';

class Competition extends Component {

  constructor(props) {

    super(props);

    this.refresh = this.refresh.bind(this);

    this.state = {
      challengeGroups: [],
      competition: null,
      competitionId: props.match.params.competitionId,
      score: 0,
      siteBranding: "Scoreboard",
      status: 'NOT_STARTED',
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

    var self = this;

    setInterval(function() {
      self.loadCompetition(self.state.competitionId);
    }, 60000)
  }
  async componentWillReceiveProps(props) {
    if (props.match.params.competitionId != this.state.competitionId) {
      var competitionId = props.match.params.competitionId;
      await this.loadCompetition(competitionId);
      this.setState({
        competitionId: competitionId,
        score: 0
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
        score: res.data.score,
        status: res.data.status
      });
    }
  }
  refresh() {
    this.loadCompetition(this.state.competitionId);
  }
  render() {

    var self = this;

    return (
      <div>

        <CompetitionHeader competitionId={this.state.competitionId} siteBranding={this.state.siteBranding} username={this.state.username} score={this.state.score} status={this.state.status} />

        <Switch>
          <Route exact path='/competition/:competitionId' render={(routeProps) => { return <CompetitionMain competitionId={routeProps.competitionId} competition={self.state.competition} challenges={self.state.challenges} /> }}/>
          <Route path='/competition/:competitionId/challenges' render={(routeProps) => { return <ChallengesMain challenges={self.state.challengeGroups} competitionId={routeProps.match.params.competitionId} onChange={this.refresh} /> }} />
          <Route exact path='/competition/:competitionId/leaderboard' render={(routeProps) => { return <Leaderboard competitionId={routeProps.match.params.competitionId} /> }} />
        </Switch>
      </div>
    )
  }
}

export default Competition;
