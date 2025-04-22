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

  return (
    <div className="app">

      <h1>DataDrip Test</h1>
      <hr />
      <br/>
      <h2 className="subheader">Please insert a photo of your face in natural lighting from shoulders up</h2>
      <br/>
      <input type="file" />
      
      <button>Upload</button>
      
      <Accept />
      <hr />

    
      {/* <h1 className="introduction">This is an AI-powered fashion assistant that helps you create the perfect outfit for any occasion! </h1>
      <h1 className="introduction">Simply upload an image of a clothing item, and the program will analyze its style, color, and fit, then recommend complementary pieces from your wardrobe or suggest new ones to complete your look. </h1>
      <h1 className="introduction">Whether you're dressing for a formal event, a casual day out, or a business meeting, the app provides outfit suggestions tailored to the occasion.</h1>
      <h1 className="introduction">With real-time feedback on how well your outfit matches the event, you'll always step out in style with confidence!</h1> */}
      
      
      

      
    </div>


    
  );
}



export default App;
