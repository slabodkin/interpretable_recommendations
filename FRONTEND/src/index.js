// djr/FRONTEND/src/index.js
import React from 'react';
import ReactDOM from 'react-dom';
import App from './App';

import { BrowserRouter } from "react-router-dom"

import ApolloClient from 'apollo-boost';
// import ApolloClient from 'apollo-client';
import { ApolloProvider } from '@apollo/react-hooks';
import { setContext } from 'apollo-link-context'
import { createHttpLink } from 'apollo-link-http'
import { InMemoryCache } from 'apollo-cache-inmemory'

import { AUTH_TOKEN } from './constants'


// const httpLink = createHttpLink({
//   uri: 'http://127.0.0.1:8000/graphql',
// })
// const authLink = setContext((_, { headers }) => {
//   const token = localStorage.getItem(AUTH_TOKEN)
//   return {
//     headers: {
//       ...headers,
//       authorization: token ? `JWT ${token}` : ''
//     }
//   }
// })
// const apiclient = new ApolloClient({
//     link: authLink.concat(httpLink), 
//     cache: new InMemoryCache(),
//   });

const apiclient = new ApolloClient({
    uri: 'http://127.0.0.1:8000/graphql',
    request: (operation) => {
      const token = localStorage.getItem(AUTH_TOKEN)
      operation.setContext({
        headers: {
          authorization: token ? `JWT ${token}` : ''
        }
      })
    }
  });

const Init = () => (
    <ApolloProvider client={apiclient}>
        <BrowserRouter>
            <App ></App>
        </BrowserRouter>
    </ApolloProvider>
)

ReactDOM.render( <Init ></Init>, document.getElementById('root'))

