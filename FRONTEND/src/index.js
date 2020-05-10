// djr/FRONTEND/src/index.js
import React from 'react';
import ReactDOM from 'react-dom';
import App from './App';

import { BrowserRouter } from "react-router-dom"

import ApolloClient from 'apollo-boost';
import { ApolloProvider } from '@apollo/react-hooks';


/*
    our api client will make request to thils adress.
    at      ~/Blog/djr/djr/urls.py
*/
const apiclient = new ApolloClient({
    uri: 'http://127.0.0.1:8000/graphql',
  });
const Init = () => (
    <ApolloProvider client={apiclient}>
        <BrowserRouter>
            <App ></App>
        </BrowserRouter>
    </ApolloProvider>
)

ReactDOM.render( <Init ></Init>, document.getElementById('root'))

