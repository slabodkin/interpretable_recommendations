import React from "react";
import { Route, Switch, Link } from "react-router-dom"
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
                <Route exact path="/user/id-:id" component={UserPage} ></Route>
            </Switch>
        </div>
    )
}
export default App

// import Apollo framework query hook
import { useQuery } from '@apollo/react-hooks';

// import our queries previously defined
import { MOVIE_QUERY, MOVIE_LIST_QUERY, USER_QUERY } from "./query"


const MainPage = (props) => {
    const { loading, error, data } = useQuery(MOVIE_LIST_QUERY);
    let current_user_id = 1;
    // when query starts, loading will be true until the response will back.
    // At this time this will be rendered on screen
    if (loading) return <div>Loading</div>
    
    // if response fail, this will be rendered
    if (error) return <div>Unexpected Error: {error.message}</div>
    //if query succeed, data will be available and render the data
    return(
        <div className="main-page">
            <Link to={`/user/id-${current_user_id}`} className="user-profile-button" >User profile</Link>
            {data && data.movieList &&
                data.movieList.map(movie => (
                    <div className="movie-card" key={movie.slug}>
                        <img 
                            className="movie-card-image"
                            src={movie.posterUrl} 
                            alt={movie.name + " poster"} 
                            title={movie.name + " poster"} 
                        />
                        <p className="movie-card-name">{movie.name}</p>
                        <Link to={`/movie/${movie.slug}`} className="movie-card-link" />
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


const UserPage = (props) => {
    // uncomment to see which props are passed from router
    //console.log(props)
    // due to we make slug parameter dynamic in route component,
    // urlParameters will look like this { slug: 'slug-of-the-selected-movie' }
    const urlParameters = props.match.params
    const { loading, error, data } = useQuery(USER_QUERY, { 
        variables:{userId:urlParameters.id}
    });
    if (loading) return <div>Loading</div>
    if (error) return <div>Unexpected Error: {error.message}</div>
    console.log(data.user)
  
    return (
        <div className="user-page">
        <Link to="/" className="back-button" >Main Page</Link>
            {data && data.user && 
                <div className="user-page-box">
                    <div className="user-page-info">
                        <h1>{data.user.name}</h1>
                        <p>Birth date: {data.user.birthdate}</p>
                        <p>Age: {data.user.age}</p>
                        <p>Gender: {data.user.gender}</p>
                    </div>
                </div>
            }
        </div>
    )
}


