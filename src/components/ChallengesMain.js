
import React, { Component } from 'react';
import  { Link, Route, Switch } from 'react-router-dom';

import Challenge from './Challenge';
import ChallengesSidebar from './ChallengesSidebar';

/**
Component ChallengesMain
props: competitionId, competitionId, challenges
*/
class ChallengesMain extends Component {

  constructor(props) {

    super(props);

    this.state = {
      challenges: props.challenges,
      competitionId: props.competitionId,
      currentChallengeId: 0
    }
  }

  componentDidMount() {
    console.log("ChallengesMain did mount.")
  }

  componentWillReceiveProps(props) {
    console.log("ChallengesMain will receive props");
    console.log(props);
    this.setState({
      challenges: props.challenges,
      competitionId: props.competitionId
    });
  }

  render() {
    return (
      <div>
        <div className="columns">
          <div className="column col-3">
            <ChallengesSidebar challenges={this.state.challenges} competitionId={this.state.competitionId} />
          </div>
          <div className="column col-9">
            <Switch>
              <Route exact path='/competition/:competitionId/challenges' render={(routeProps) => { return (<p>Please choose a challenge from the left.</p>) }} />
              <Route exact path='/competition/:competitionId/challenges/:challengeId' render={(routeProps) => { return (<Challenge challengeId={routeProps.match.params.challengeId} competitionId={routeProps.match.params.competitionId} />) }} />
            </Switch>
          </div>
        </div>
      </div>
    )
  }
}

export default ChallengesMain;
