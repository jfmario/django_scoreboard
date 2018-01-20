
import React, { Component } from 'react';
import  { Link, Route, Switch } from 'react-router-dom';

import axios from 'axios';

class Leaderboard extends Component {

  constructor(props) {

    super(props);

    this.state = {
      competitionId: props.competitionId,
      leaderboard: [],
      maxScore: 100
    };
  }

  componentDidMount() {

    var self = this;
    self.updateLeaderboard();

    setInterval(function() {
      self.updateLeaderboard();
    }, 60000);
  }

  componentWillReceiveProps(props) {
    this.setState({
      competitionId: props.competitionId
    });
  }

  async updateLeaderboard() {
    var res = await axios.post(`/api/competition/${this.state.competitionId}/leaderboard`);
    this.setState({
      leaderboard: res.data.scores,
      maxScore: res.data.maxScore
    });
  }

  render() {
    return (
      <div className="card">
        <div className="card-header">
          <div className="card-title h5">Leaderboard</div>
        </div>
        <div className="card-body">
          <table className="table">
            <thead>
              <tr>
                <th>Username</th>
                <th>Score</th>
                <th>Visualization</th>
              </tr>
            </thead>
            <tbody>
              {this.state.leaderboard.map((l) => (
                <tr>
                  <td>{l.username}</td>
                  <td>{l.score}</td>
                  <td>
                    <div className="bar-item" style={{color:'#f0f',width:`${100 * (l.score / this.state.maxScore)}%`,background:'#88b'}}>{`${parseInt(100 * (l.score / this.state.maxScore))}%`}</div>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    )
  }
}

export default Leaderboard;
