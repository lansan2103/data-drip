import React from 'react';
import ReactDOM from 'react-dom/client';
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import './index.css';

import App from './App.js';


import Page1 from './Page1';
import Page2 from './Page2';

import Layout from './Layout';


const root = ReactDOM.createRoot(document.getElementById('root'));

root.render(
  <React.StrictMode>
    <BrowserRouter>
      <Routes>
        <Route path='/' element={<Layout />}>
          <Route index element={<App />} />
          <Route path="page1" element={<Page1 />} />
          <Route path="page2" element={<Page2 />} /> 
        </Route>
      </Routes>
    </BrowserRouter>
  </React.StrictMode>
);

