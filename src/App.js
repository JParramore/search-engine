import React from 'react';
import './App.css';
import SearchContainer from './Components/SearchContainer';

function App() {

  // fetch('/search').then(res => res.text()).then(text => console.log(text))
  return (
    <SearchContainer />
  );
}

export default App;