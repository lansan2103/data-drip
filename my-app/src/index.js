import React from 'react';
import ReactDOM from 'react-dom/client';
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import './index.css';

import App from './App.js';


import About from './about.js';

import Layout from './Layout';


const root = ReactDOM.createRoot(document.getElementById('root'));

root.render(
  <React.StrictMode>
    <BrowserRouter>
      <Routes>
        <Route path='/' element={<Layout />}>
          <Route index element={<About />} />
          <Route path="test" element={<App />} /> 
        </Route>
      </Routes>
    </BrowserRouter>
  </React.StrictMode>
);

