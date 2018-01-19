
import React, { Component } from 'react';
import  { Link } from 'react-router-dom';

/**
Component CompetitionHeader
props: competitionId, siteBranding, username
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
          <Link className="btn btn-link" to={`/competition/${this.props.competitionId}/challenges`}>Challenges</Link>
          <Link className="btn btn-link" to={`/competition/${this.props.competitionId}/leaderboard`}>Leaderboard</Link>

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
        </section>
      </header>
    )
  }
}

export default CompetitionHeader;
