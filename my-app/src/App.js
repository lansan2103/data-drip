import React, { useState } from 'react';
import { useDropzone } from 'react-dropzone';
import './App.css';

function Accept({ setFile }) {
  const { acceptedFiles, getRootProps, getInputProps } = useDropzone({
    accept: {
      'image/jpeg': [],
      'image/png': []
    },
    onDrop: (acceptedFiles) => {
      if (acceptedFiles.length > 0) {
        setFile(acceptedFiles[0]);
      }
    }
  });

  const fileList = acceptedFiles.map(file => (
    <li key={file.path}>
      {file.path} - {file.size} bytes
    </li>
  ));

  return (
    <section className="container">
      <div {...getRootProps({ className: 'dropzone' })}>
        <input {...getInputProps()} />
        <p>Drag 'n' drop an image here, or click to select</p>
      </div>
      <aside>
        <h4 className = 'subheader'>Selected File:</h4>
        <ul>{fileList}</ul>
      </aside>
    </section>
  );
}

function App() {
  const [file, setFile] = useState(null);
  const [season, setSeason] = useState('');
  const [palette, setPalette] = useState([]);
  const [links, setLink] = useState({});

  const handleUpload = async () => {
    if (!file) {
      alert('Please select a file first.');
      return;
    }

    const formData = new FormData();
    formData.append('file', file);

    try {
      const response = await fetch('http://127.0.0.1:5000/upload', {
        method: 'POST',
        body: formData
      });

      if (!response.ok) {
        throw new Error('Unable to detect face. Please try another image.');
      }

      const data = await response.json();
      console.log(data);  // <-- ADD THIS
      console.log('Data received from backend:', data); // Add this line to see the whole data object
      console.log('Palette:', data.palette);  // Specifically print the palette
      setSeason(data.season);
      setPalette(data.palette);
      setLink(data.links);

    } catch (error) {
      alert(error.message);
    }
  };

  return (
    <div className="app">
      <h1 className="title">DataDrip Test</h1>
      
      <hr />

      <h2 className="subheader">Upload a clear photo of your face</h2>

      <Accept setFile={setFile} />
      <button onClick={handleUpload} className="upload-button" style={{marginLeft: '740px'}}>Upload</button>

      {season && (
        <div className="results">
          <h2>Detected Season: {season}</h2>
          <h3>Recommended Palette:</h3>
          <div className="palette-grid">
            {palette.map(([colorName, hexValue], index) => (
              <div key={index} className="color-box">
                <div className="color-swatch" style={{ backgroundColor: hexValue }}></div>
                <div className="color-name">{colorName}</div>
              </div>
            ))}
          </div>
        </div>
      )}

      {links.top && links.bottom && links.shoes && (
       <div className="results">
        <h3>Outfit Links</h3>
        <div>Top: {links.top.url}</div>
        <div>Bottom: {links.bottom.url}</div>
        <div>Shoes: {links.shoes.url}</div>
       </div>
      )}
      


    </div>
  );
}

export default App;