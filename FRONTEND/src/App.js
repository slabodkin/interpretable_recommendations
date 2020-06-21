import React from "react";
import { Route, Switch, Link } from "react-router-dom"
import Login from './Login'
import { AUTH_TOKEN } from './constants.js'
import "./App.css"


const App = () => {
  return (
    <div className="App">
      <Switch>
        <Route exact path="/" component={MainPage} ></Route>
        // colon before slug means it is a dynamic value
        // that makes slug parameter anything
        // like: /movie/the-matrix-1999   or /movie/anything
        <Route exact path="/movie/:slug" component={MoviePage} ></Route>
        <Route exact path="/item/:slug" component={ItemPage} ></Route>
        <Route exact path="/profile" component={UserPage} ></Route>
        <Route exact path="/login" component={Login} />
      </Switch>
    </div>
  )
}
export default App

// import Apollo framework query hook
import { useQuery } from '@apollo/react-hooks';

// import our queries previously defined
import { ITEM_QUERY, RANDOM_ITEM_LIST_QUERY, USER_QUERY, ME_QUERY, RECOMMENDATIONS_QUERY } from "./query"


const MainPage = (props) => {
  const authToken = localStorage.getItem(AUTH_TOKEN)
  // console.log(authToken);
  let n_items = 10;
  const { loading, error, data } = useQuery(RANDOM_ITEM_LIST_QUERY, { 
    variables:{n:n_items}
  });
  // let current_user_email = 1;
  // when query starts, loading will be true until the response will back.
  // At this time this will be rendered on screen
  if (loading) return <div>Loading</div>
  
  // if response fail, this will be rendered
  if (error) return <div>Unexpected Error: {error.message}</div>
  //if query succeed, data will be available and render the data
  return(
    <div className="main-page">
      {authToken ?
        <Link to={`/profile`} className="user-profile-button" >User profile</Link>
       :
        <Link to={`/Login`} className="user-profile-button" >Login</Link>
      }

      {authToken &&
        <div
          className="user-profile-button"
          onClick={() => {
            localStorage.removeItem(AUTH_TOKEN)
            props.history.push(`/`)
          }}
        >
          Logout
        </div>
      }
      {data && data.itemList &&
        data.itemList.map(item => (
          <div className="item-card" key={item.slug}>
            <p className="item-card-title">{item.title}</p>
            <p className="item-card-description">{item.author}, {item.year}</p>
            <Link to={`/item/${item.slug}`} className="item-card-link" />
          </div>
        ))
      }
    </div>
  )
}

const MoviePage = (props) => {
  // uncomment to see which props are passed from router
  //console.log(props)
  // due to we make slug parameter dynamic in route component,
  // urlParameters will look like this { slug: 'slug-of-the-selected-movie' }
  const urlParameters = props.match.params
  const { loading, error, data } = useQuery(MOVIE_QUERY, { 
    variables:{slug:urlParameters.slug}
  });
  if (loading) return <div>Loading</div>
  if (error) return <div>Unexpected Error: {error.message}</div>
  
  return (
    <div className="movie-page">
    <Link to="/" className="back-button" >Main Page</Link>
      {data && data.movie && 
        <div className="movie-page-box">
          <img 
            className="movie-page-image"
            src={data.movie.posterUrl} 
            alt={data.movie.name + " poster"} 
            title={data.movie.name + " poster"} 
          />
          <div className="movie-page-info">
            <h1>{data.movie.name}</h1>
            <p>Year: {data.movie.year}</p>
            <br />
            <p>{data.movie.summary}</p>
          </div>
        </div>
      }
    </div>
  )
}


const ItemPage = (props) => {
  // uncomment to see which props are passed from router
  //console.log(props)
  // due to we make slug parameter dynamic in route component,
  // urlParameters will look like this { slug: 'slug-of-the-selected-movie' }
  const urlParameters = props.match.params
  const { loading, error, data } = useQuery(ITEM_QUERY, { 
    variables:{itemId:urlParameters.slug}
  });
  if (loading) return <div>Loading</div>
  if (error) return <div>Unexpected Error: {error.message}</div>
  
  return (
    <div className="movie-page">
    <Link to="/" className="back-button" >Main Page</Link>
      {data && data.item && 
        <div className="movie-page-box">
          <div className="movie-page-info">
            <h1>{data.item.title}</h1>
            <p>Year: {data.item.year}</p>
            <p>Author: {data.item.author}</p>
            <br />
            <p>{data.item.summary}</p>
          </div>
        </div>
      }
    </div>
  )
}


const UserPage = (props) => {
  // uncomment to see which props are passed from router
  // console.log(props)
  
  const { loading, error, data } = useQuery(ME_QUERY, {});
  const { loading: loading2, error: error2, data: data2 } = useQuery(RECOMMENDATIONS_QUERY, {});
  
  let user = (!loading && !error && data) ? data.me : null;
  let recommendations = (!loading2 && !error2 && data2) ? data2.recommendations : null;
  if (loading) return <div>Loading</div>
  if (error) return <div>Unexpected Error: {error.message}</div>
  if (loading2) return <div>Loading</div>
  if (error2) return <div>Unexpected Error: {error2.message}</div>
  
  return (
    <div className="user-page">
    <Link to="/" className="back-button" >Main Page</Link>
      {user && 
        <div className="user-page-box">
          <div className="user-page-info">
            <h1>Name: {user.name}</h1>
            <div>Birth date: {user.birthdate}</div>
            <div>Age: {user.age}</div>
            <div>Gender: {user.gender}</div>
            <div>Items: 
              {user.rates &&
                user.rates.map(rate => (
                  <p  className="user-page-movie-entry" key={rate.item.slug}>
                    <Link to={`/item/${rate.item.slug}`} className="user-page-movie-entry-link">
                      {rate.item.title}, {rate.item.author}, {rate.item.year}, rate: {rate.score}
                    </Link>
                  </p>
                ))
              }
            </div>
            <div>You might also like: 
              {recommendations &&
                recommendations.map(item => (
                  <p  className="user-page-movie-entry" key={item.slug}>
                    <Link to={`/item/${item.slug}`} className="user-page-movie-entry-link">
                      {item.title}, {item.author}, {item.year}
                    </Link>
                  </p>
                ))
              }
            </div>
          </div>
        </div>
      }
    </div>
  )
}


