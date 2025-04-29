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
        <h4>Accepted files:</h4>
        <ul>{acceptedFileItems}</ul>
        <h4>Rejected files:</h4>
        <ul>{fileRejectionItems}</ul>
      </aside>
    </section>
  );
}
function App() {
  const [file, setFile] = useState(null);

  const handleChange = (event) => {
    setFile(event.target.files[0]);
  };

  const handleUpload = async () => {
    if (!file) return alert("Please select a file first.");

    const formData = new FormData();
    formData.append('file', file);

    const response = await fetch('http://127.0.0.1:5000/upload', {
      method: 'POST',
      body: formData
    });

    if (response.ok) {
      alert("Upload successful!");
    } else {
      alert("Upload failed.");
    }
  };

  return (
    <div className="app">

      <h1 className= "title">DataDrip Test</h1>
      <hr />
      <h2 className="subheader">Please insert a photo of your face in natural lighting from shoulders up</h2>

      <Accept />
      <hr />
    </div>
  );
}




export default App;
