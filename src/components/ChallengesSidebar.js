
import React, { Component } from 'react';
import  { Link } from 'react-router-dom';

import Collapsible from 'react-collapsible';

/**
Component ChallengesSidebar
props: challenges, competitionId
*/
class ChallengesSidebar extends Component {

  constructor(props) {

    super(props);

    this.state = {
      challengeGroups: props.challenges,
      competitionId: props.competitionId
    };
  }

  componentWillReceiveProps(props) {
    this.setState({
      challengeGroups: props.challenges,
      competitionId: props.competitionId
    });
  }

  render() {
    return (
      <div className="card">
        <div className="card-header">
          <div className="card-title h4">Challenges</div>
        </div>
        <div className="card-body">
          {!!(this.state.challengeGroups) && this.state.challengeGroups.map((cg, index) => (
            <Collapsible trigger={cg.group}>
              <ul className="menu">
                {cg.challenges.map((c) => (
                  <li className="menu-item">
                    <Link to={`/competition/${this.state.competitionId}/challenges/${c.id}`}>
                      {c.name}
                    </Link>
                  </li>
                ))}
              </ul>
            </Collapsible>
          ))}
        </div>
      </div>
    )
  }
}

export default ChallengesSidebar;
