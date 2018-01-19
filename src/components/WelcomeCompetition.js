
import React, { Component } from 'react';
import  { Link } from 'react-router-dom';

import moment from 'moment';

/**
Component WelcomeCompetition
props: competition, competitionId
*/
class WelcomeCompetition extends Component {

  constructor(props) {

    super(props);

    this.state = {
      descriptionHtml: { __html: props.competition.description },
      welcomeHtml: { __html: props.competition.welcome }
    };
  }

  componentDidMount() {
    console.log("WelcomeCompetition did mount.");
    console.log(this.state);
  }

  componentWillReceiveProps(props) {
    console.log("WelcomeMain will receive props.");
    console.log(props);
    this.setState({
      descriptionHtml: { __html: props.competition.description },
      welcomeHtml: { __html: props.competition.welcome }
    })
  }

  render() {
    return (
      <div className="card">
        <div className="card-header">
          <div className="card-title h5">{this.props.competition.name}</div>
        </div>
        <div className="card-body">

          <div dangerouslySetInnerHTML={this.state.welcomeHtml} />

          {!!(this.props.competition.status == 'NOT_STARTED') &&
            <p className="text-gray">Competition begins {moment(this.props.competition.startTime).fromNow()}</p>
          }
          {!!(this.props.competition.status == 'ACTIVE') &&
            <div>

              <p className="text-success">Competition ends {moment(this.props.competition.endTime).fromNow()}</p>

              <Link className="btn btn-lg btn-primary" to={`/competition/${this.props.competitionId}/challenges`}>View Challenges</Link>
            </div>
          }
          {!!(this.props.competition.status == 'OVER') &&
            <p className="text-error">This competition has ended.</p>
          }
        </div>
      </div>
    )
  }
}

export default WelcomeCompetition;
