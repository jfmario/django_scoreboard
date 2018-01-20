
import React, { Component } from 'react';
import  { Link } from 'react-router-dom';

import axios from 'axios';

/**
Component Challenge
props: challengeId, competitionId, onChange
*/
class Challenge extends Component {

  constructor(props) {

    super(props);

    this.getHint = this.getHint.bind(this);
    this.handleAnswerChange = this.handleAnswerChange.bind(this);
    this.handleSubmit = this.handleSubmit.bind(this);

    this.state = {
      answer: '',
      challenge: null,
      challengeId: props.challengeId,
      competitionId: props.competitionId,
      hintHtml: { __html: '' },
      questionHtml: { __html: '' }
    };
  }

  componentDidMount() {
    this.getChallenge(this.state.competitionId, this.state.challengeId);
  }

  componentWillReceiveProps(props) {
    if (props.challengeId != this.state.challengeId) {
      this.setState({
        answer: '',
        challenge: null,
        challengeId: props.challengeId,
        competitionId: props.competitionId
      });
      this.getChallenge(props.competitionId, props.challengeId);
    }
  }

  handleAnswerChange(e) {
    this.setState({
      answer: e.target.value
    });
  }
  async handleSubmit(e) {

    e.preventDefault();

    var res = await axios.post(`/api/competition/${this.state.competitionId}/challenge/${this.state.challengeId}/submit`, {
      answer: this.state.answer
    });
    this.setState({
      answer: '',
      challenge: res.data,
      questionHtml: { __html: res.data.question }
    });
    if (res.data.hintPurchased) {
      this.setState({
        hintHtml: { __html: res.data.hint }
      });
    }
    this.props.onChange();
  }

  async getChallenge(competitionId, challengeId) {
    var res = await axios.post(`/api/competition/${competitionId}/challenge/${challengeId}`);
    this.setState({
      challenge: res.data,
      questionHtml: { __html: res.data.question }
    });
    if (res.data.hintPurchased) {
      this.setState({
        hintHtml: { __html: res.data.hint }
      });
    }

  }
  async getHint(e) {

    e.preventDefault();

    var res = await axios.post(`/api/competition/${this.state.competitionId}/challenge/${this.state.challengeId}/hint`);
    this.setState({
      challenge: res.data,
      questionHtml: { __html: res.data.question }
    });
    if (res.data.hintPurchased) {
      this.setState({
        hintHtml: { __html: res.data.hint }
      });
    }
    this.props.onChange();
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

            {!!(this.state.challenge.dataFileRef) &&
              <p>
                <b>Attached File: </b>
                <a href={`/${this.state.challenge.dataFileRef}`} download>/{this.state.challenge.dataFileRef}</a>
              </p>
            }

            {!!(this.state.challenge.solved == false) &&
              <div>

                <br />
                
                <p className="text-primary">Solve this challenge to gain {this.state.challenge.points} points.</p>
              </div>
            }

            {!!(this.state.challenge.hasHint && this.state.challenge.solved == false) &&
              <div>

                <h5>Hint</h5>

                {!!(this.state.challenge.hintPurchased) &&
                  <div dangerouslySetInnerHTML={this.state.hintHtml} />
                }
                {!!(this.state.challenge.hintPurchased == false) &&
                  <div>
                    <p>Viewing the hint will cost {this.state.challenge.hintCost} points.</p>
                    <p>
                      <button className="btn badge" onClick={this.getHint} data-badge={`-${this.state.challenge.hintCost}`}>
                        View Hint
                      </button>
                    </p>
                  </div>
                }
              </div>
            }

            <h5>Answer</h5>

            {!!(this.state.challenge.solved == false) &&
              <div className="form" onSubmit={this.handleSubmit}>

                {!!(this.state.challenge.questionType == 'ShortAnswer') &&
                  <input className="form-input" type="text" value={this.state.answer} onChange={this.handleAnswerChange} />
                }
                {!!(this.state.challenge.questionType == 'TextAnswer') &&
                  <textarea className="form-input" type="textarea" value={this.state.answer} onChange={this.handleAnswerChange} />
                }
                {!!(this.state.challenge.questionType == 'MultipleChoice') &&
                  <select className="form-select" type="text" value={this.state.answer} onChange={this.handleAnswerChange}>
                     {this.state.challenge.choices.map((o) =>(
                       <option>{o}</option>
                     ))}
                  </select>
                }

                <p className="text-gray">
                  An incorrect answer will cost {this.state.challenge.wrongAnswerCost} points.
                </p>

                <button className="btn btn-primary" type="submit" onClick={this.handleSubmit}>Submit Answer</button>

                <br />
                <br />

                {!!(this.state.challenge.wrongAnswerHistory.length > 0) &&
                  <div>

                    <h6>Wrong Answers</h6>

                    <ul>
                      {this.state.challenge.wrongAnswerHistory.map((w) => (
                        <li className="text-error">{w}</li>
                      ))}
                    </ul>
                  </div>
                }
              </div>
            }
            {!!(this.state.challenge.solved) &&
              <p className="text-success">You have solved this question!</p>
            }
          </div>
        }
      </div>
    )
  }
}

export default Challenge;
