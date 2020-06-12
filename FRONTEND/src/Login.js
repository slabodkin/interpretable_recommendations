import React, { Component } from 'react'
import { Mutation } from 'react-apollo'
// import { Mutation } from 'apollo-boost'
import { useQuery } from '@apollo/react-hooks';

// import Apollo framework query hook
import { AUTH_TOKEN } from './constants'
import { USERID_BY_EMAIL_QUERY } from "./query"
import { SIGNUP_MUTATION } from "./query"
import { LOGIN_MUTATION } from "./query"



class Login extends Component {

  constructor(props) {
    super(props);
    this.state = {
      login: true, // switch between Login and SignUp
      email: '',
      password: '',
      name: '',
    };
  }

  render() {
    const { login, email, password, name } = this.state
    return (
      <div className="centered-box">
        <h2>{login ? 'Login' : 'Sign Up'}</h2>
        <div>
          {!login && (
            <input
              value={name}
              onChange={e => this.setState({ name: e.target.value })}
              type="text"
              placeholder="Your name"
            />
          )}
          <input
            value={email}
            onChange={e => this.setState({ email: e.target.value })}
            type="text"
            placeholder="Your email address"
          />
          <input
            value={password}
            onChange={e => this.setState({ password: e.target.value })}
            type="text" // TODO: change type back to "password" 
            placeholder={login? "Your password" : "Choose a safe password"}
          />
        </div>
        <div>
          <Mutation
            mutation={login ? LOGIN_MUTATION : SIGNUP_MUTATION}
            // mutation={login ? USERID_BY_EMAIL_QUERY : USERID_BY_EMAIL_QUERY}
            variables={login ? { email, password } : { email, password, name }}
            onCompleted={data => {
              this._confirm(data);
            }}
          >
            {mutation => (
              <div className="default-button" onClick={mutation}>
                {(login ? 'login' : 'create account')}
              </div>
            )}
          </Mutation>
          <div
            className="default-button"
            onClick={() => this.setState({ login: !login })}
          >
            {login
              ? 'need to create an account?'
              : 'already have an account?'}
          </div>
        </div>
      </div>
    )
  }

  // _confirm = async () => {
  //   // ... you'll implement this 🔜
  // }


  _confirm(data) {
    const { token } = this.state.login ? data.tokenAuth : data.signup
    this._saveUserData(token)
    this.props.history.push(`/`)
     // const { loading, error, data } = useQuery(USERID_BY_EMAIL_QUERY, { 
        // variables:{email:this.state.email}
    // });
    // if (loading) return <div>Loading</div>
    // if (error) return <div>Unexpected Error: {error.message}</div>
    // console.log(data.useridByEmail)
  
    // ... you'll implement this 🔜
  }

  _saveUserData(token) {
    localStorage.setItem(AUTH_TOKEN, token)
  }
}

export default Login