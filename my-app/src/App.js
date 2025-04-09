// import {useState} from 'react';
// import React, {Component} from 'react';
// import './App.css';
// import {useDropzone} from 'react-dropzone';
// /*import axios from 'axios';

// console.log("App component loaded");
//       <button onClick={this.fileUploadHandler}>Upload</button>
// class App extends Component{
//   state = {
//     selectedFile: null
//   }

//   fileSelectedHandler = event => {
//     console.log(event.target.files(0));
//   }
// }
// fileUploadHandler = () => {
//   axios.post('')
// }*/

// function App() {
// const [display, setDisplay] = useState(0);
// function addNum(){
//   setDisplay(display+1);
// }  
// function subNum(){
//   setDisplay(display-1);
// }

// useDrop({
//   accept: {
//     'image/jpg': ['.jpg']
//   }
// })

// function Accept(props) {
//   const {
//     acceptedFiles,
//     fileRejections,
//     getRootProps,
//     getInputProps
//   } = useDropzone({
//     accept: {
//       'image/jpeg': [],
//       'image/png': []
//     }
//   });

//   const acceptedFileItems = acceptedFiles.map(file => (
//     <li key={file.path}>
//       {file.path} - {file.size} bytes
//     </li>
//   ));

//   const fileRejectionItems = fileRejections.map(({ file, errors }) => (
//     <li key={file.path}>
//       {file.path} - {file.size} bytes
//       <ul>
//         {errors.map(e => (
//           <li key={e.code}>{e.message}</li>
//         ))}
//       </ul>
//     </li>
//   ));

//   return (
//     <div>
//     <div className = 'app'>
//       <div className = 'add'>
//         <button onClick = {addNum}>+</button>
//       </div>
//       <h1 className = 'header'>DataDrip!</h1>
//       <h1> Welcome to DataDrip!</h1>
      
      
//       <h2 className = 'subheader'> Please insert a .jpg photo of your face in natural lighting from shoulders up</h2>
//       <input type="file"></input>
//             <button onClick>Upload</button>
//       </div>

//       <section className="container">
//       <div {...getRootProps({ className: 'dropzone' })}>
//         <input {...getInputProps()} />
//         <p>Drag 'n' drop some files here, or click to select files</p>
//         <em>(Only *.jpeg and *.png images will be accepted)</em>
//       </div>
//       <aside>
//         <h4>Accepted files</h4>
//         <ul>{acceptedFileItems}</ul>
//         <h4>Rejected files</h4>
//         <ul>{fileRejectionItems}</ul>
//       </aside>
//     </section>

//     <Accept />
//     </div>
//   );
// }


// export default App;

import React, { useState } from 'react';
import { useDropzone } from 'react-dropzone';
import './App.css';

function Accept() {
  const {
    acceptedFiles,
    fileRejections,
    getRootProps,
    getInputProps
  } = useDropzone({
    accept: {
      'image/jpeg': [],
      'image/png': []
    }
  });

  const acceptedFileItems = acceptedFiles.map(file => (
    <li key={file.path}>
      {file.path} - {file.size} bytes
    </li>
  ));

  const fileRejectionItems = fileRejections.map(({ file, errors }) => (
    <li key={file.path}>
      {file.path} - {file.size} bytes
      <ul>
        {errors.map(e => (
          <li key={e.code}>{e.message}</li>
        ))}
      </ul>
    </li>
  ));

  return (
    <section className="container">
      <div {...getRootProps({ className: 'dropzone' })}>
        <input {...getInputProps()} />
        <p>Drag 'n' drop some files here, or click to select files</p>
        <em>(Only *.jpeg images will be accepted)</em>
      </div>
      <aside>
        <h4>Accepted files</h4>
        <ul>{acceptedFileItems}</ul>
        <h4>Rejected files</h4>
        <ul>{fileRejectionItems}</ul>
      </aside>
    </section>
  );
}

function App() {
  const [display, setDisplay] = useState(0);

  const addNum = () => setDisplay(display + 1);
  const subNum = () => setDisplay(display - 1);

  return (
    <div className="app">
      <div className="add">
        <button onClick={addNum}>+</button>
        <button onClick={subNum}>-</button>
        <p>{display}</p>
      </div>
      <h1 className="header">DataDrip!</h1>
      <h2 className="subheader">Please insert a .jpeg photo of your face in natural lighting from shoulders up</h2>
      <input type="file" />
      <button>Upload</button>

      <Accept />
    </div>
  );
}

export default App;
