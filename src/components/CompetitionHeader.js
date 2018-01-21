
import React, { Component } from 'react';
import  { Link } from 'react-router-dom';

import moment from 'moment';

/**
Component CompetitionHeader
props: competitionId, siteBranding, username, score, status
*/
class CompetitionHeader extends Component {

  constructor(props) {

    super(props);

    this.preventNav = this.preventNav.bind(this);
  }

  preventNav(e) {
    e.preventDefault();
  }

  render() {
    return (
      <header className="navbar">
        <section className="navbar-section">

          <Link className="mr-2 navbar-brand" to={'/'}>{this.props.siteBranding}</Link>
          <Link className="btn btn-link" to={`/competition/${this.props.competitionId}`}>Competition</Link>
          {!!(this.props.status == 'ACTIVE') &&
            <Link className="btn btn-link" to={`/competition/${this.props.competitionId}/challenges`}>Challenges</Link>
          }
          {!!(this.props.status != 'NOT_STARTED') &&
            <Link className="btn btn-link" to={`/competition/${this.props.competitionId}/leaderboard`}>Leaderboard</Link>
          }

          {!!(this.props.username) &&
            <div className="dropdown">

              <a className="btn btn-link dropdown-toggle" href="#" tabIndex="0" onClick={this.preventNav}>{this.props.username}
                <i className="icon icon-caret"></i>
              </a>

              <ul className="menu">
                <li className="menu-item">
                  <a href="/accounts/logout">Change Password</a>
                </li>
                <li className="menu-item">
                  <a href="/accounts/logout">Logout</a>
                </li>
              </ul>
            </div>
          }

          {!!(this.props.status == 'NOT_STARTED') &&
            <span className="text-gray">This competition has not yet started.</span>
          }
          {!!(this.props.status == 'ACTIVE') &&
            <span>
              <span>Score: {this.props.score}. </span>
              <span className="text-gray">Competition ends {moment(this.props.endTime).fromNow()}.</span>
            </span>
          }
          {!!(this.props.status == 'OVER') &&
            <span>
              <span>Score: {this.props.score}. </span>
              <span className="text-error">This competition has ended.</span>
            </span>
          }
        </section>
      </header>
    )
  }
}

export default CompetitionHeader;
