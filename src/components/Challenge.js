
import React, { Component } from 'react';
import  { Link } from 'react-router-dom';

import axios from 'axios';

/**
Component Challenge
props: challengeId, competitionId
*/
class Challenge extends Component {

  constructor(props) {

    super(props);

    console.log("Challenge constructor.");

    this.state = {
      challenge: null,
      challengeId: props.challengeId,
      competitionId: props.competitionId,
      questionHtml: {}
    };
  }

  componentDidMount() {
    this.getChallenge(this.state.competitionId, this.state.challengeId);
  }

  componentWillReceiveProps(props) {
    if (props.challengeId != this.state.challengeId) {
      this.setState({
        challenge: null,
        challengeId: props.challengeId,
        competitionId: props.competitionId
      });
      this.getChallenge(props.competitionId, props.challengeId);
    }
  }

  async getChallenge(competitionId, challengeId) {
    var res = await axios.post(`/api/competition/${competitionId}/challenge/${challengeId}`);
    this.setState({
      challenge: res.data,
      questionHtml: { __html: res.data.question }
    });
  }

  render() {
    return(
      <div className="card">
        {!!(this.state.challenge) &&
          <div className="card-header">
            <div className="card-title h3">{this.state.challenge.name}</div>
          </div>
        }
        {!!(this.state.challenge) &&
          <div className="card-body">

            <h4>Question</h4>

            <div dangerouslySetInnerHTML={this.state.questionHtml} />

            <h5>Hint</h5>
          </div>
        }
      </div>
    )
  }
}

export default Challenge;
