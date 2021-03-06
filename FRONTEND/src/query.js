//import our graph query parser
import gql from "graphql-tag";
// our first query will requests all movies
// with only given fields
// note the usage of gql with jsvascript string literal
// export const MOVIE_LIST_QUERY = gql`
//     query movieList{
//         movieList{
//             name, posterUrl, slug
//         }
//     }
// `
export const RANDOM_ITEM_LIST_QUERY = gql`
    query itemList($n:Int!){
        itemList(n:$n){
            id, title, year, author, summary, slug
        }
    }
`
// Note the usage of argument.
// the exclamation mark makes the slug argument as required
// without it , argument will be optional
// export const MOVIE_QUERY = gql`
//     query movie($slug:String!){
//         movie(slug:$slug){
//             id, name, year, summary, posterUrl, slug
//         }
//     }
// `
export const ITEM_QUERY = gql`
    query item($itemId:Int!){
        item(itemId:$itemId){
            id, title, year, author, summary, slug
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
          title,
          author
          year,
          summary,
          slug
        },
        score
      }
    }
  }
`
export const RECOMMENDATIONS_QUERY = gql`
  query RecommendationQuery {
    recommendations {
        title,
        author,
        year,
        slug
    }
  }
`