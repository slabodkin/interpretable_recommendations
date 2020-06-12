//import our graph query parser
import gql from "graphql-tag";
// our first query will requests all movies
// with only given fields
// note the usage of gql with jsvascript string literal
export const MOVIE_LIST_QUERY = gql`
    query movieList{
        movieList{
            name, posterUrl, slug
        }
    }
`
// Note the usage of argument.
// the exclamation mark makes the slug argument as required
// without it , argument will be optional
export const MOVIE_QUERY = gql`
    query movie($slug:String!){
        movie(slug:$slug){
            id, name, year, summary, posterUrl, slug
        }
    }
`

export const USER_QUERY = gql`
    query user($email:String!){
        user(email:$email){
            email, name, birthdate, gender
        }
    }
`


export const SIGNUP_MUTATION = gql`
  mutation SignupMutation($email: String!, $password: String!, $name: String!) {
    signup(email: $email, password: $password, name: $name) {
      token
    }
  }
`
// export const SIGNUP_MUTATION = gql`
//   mutation SignupMutation($email: String!, $password: String!, $name: String!) {
//     signup(email: $email, password: $password, name: $name) {
//       token
//     }
//   }
// `

export const LOGIN_MUTATION = gql`
  mutation LoginMutation($email: String!, $password: String!) {
    tokenAuth(email: $email, password: $password) {
      token
    }
  }
`
export const ME_QUERY = gql`
  query MeQuery {
    me {
      email,
      name,
      birthdate,
      gender,
      rates {
        item {
          name,
          year,
          slug
        },
        score
      }
    }
  }
`