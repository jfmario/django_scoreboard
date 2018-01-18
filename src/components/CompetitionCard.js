
import React, { Component } from 'react';
import  { Link } from 'react-router-dom';

import moment from 'moment';

/**
Component CompetitionCard
props: competition(.id, .name, .startTime, .endTime, .description)
*/
class CompetitionCard extends Component {

  constructor(props) {

    super(props);

    this.state = {
      descriptionHtml: { __html: props.competition.description },
      endTime: moment(props.competition.endTime),
      startTime: moment(props.competition.startTime)
    };
  }

  render() {

    var timeString = (<p className="text-gray">Begins {this.state.startTime.fromNow()}</p>);
    if (this.state.startTime.isBefore(moment())) {
      timeString = (<p className="text-success">Ends {this.state.endTime.fromNow()}</p>);
    }
    if (this.state.endTime.subtract(30, 'minutes').isBefore(moment())) {
      timeString = (<p className="text-error">Ends {this.state.endTime.fromNow()}</p>);
    }
    if (this.state.endTime.isBefore(moment())) {
      timeString = (<p className="text-error">Ended {this.state.endTime.fromNow()}</p>);
    }
    return (
      <div className="card">
        <div className="card-header">
          <div className="card-title h5">{this.props.competition.name}</div>
        </div>
        <div className="card-body">

          <div dangerouslySetInnerHTML={this.state.descriptionHtml} />

          {timeString}

          <Link className="btn btn-primary" to={`/competition/${this.props.competition.id}`}>Enter</Link>
        </div>
      </div>
    )
  }
}

export default CompetitionCard;
