import React, { useState, useEffect } from 'react';
import { useDropzone } from 'react-dropzone';
import './App.css';

// Dropzone component only selects the file
function Accept({ setFile }) {
  const { getRootProps, getInputProps } = useDropzone({
    accept: {
      'image/jpeg': [],
      'image/png': []
    },
    onDrop: (files) => {
      if (files.length > 0) setFile(files[0]);
    }
  });

  return (
    <section className="container">
      <div {...getRootProps({ className: 'dropzone' })}>
        <input {...getInputProps()} />
        <p>Drag 'n' drop an image here, or click to select</p>
      </div>
    </section>
  );
}

function App() {
  const [file, setFile] = useState(null);
  const [preview, setPreview] = useState(null);
  const [season, setSeason] = useState('');
  const [palette, setPalette] = useState([]);
  const [gender, setGender] = useState('');
  const [links, setLink] = useState({});
  const [images, setImages] = useState({});

  // make preview URL
  useEffect(() => {
    if (!file) {
      setPreview(null);
      return;
    }
    const url = URL.createObjectURL(file);
    setPreview(url);
    return () => URL.revokeObjectURL(url);
  }, [file]);

  const handleUpload = async () => {
    if (!file) return alert('Please select a file first.');
    if (!gender) return alert('Please select your gender first.');

    const formData = new FormData();
    formData.append('file', file);
    formData.append('gender', gender);

    try {
      const response = await fetch('http://localhost:5000/upload', {
        method: 'POST',
        body: formData
      });
      if (!response.ok) throw new Error('Unable to detect face. Please try another image.');

      const data = await response.json();
      console.log(data);  // <-- ADD THIS
      console.log('Data received from backend:', data); // Add this line to see the whole data object
      console.log('Palette:', data.palette);  // Specifically print the palette
      setSeason(data.season);
      setPalette(data.palette);
      setLink(data.links);
      setImages(data.images);
    } catch (error) {
      alert(error.message);
    }
  };

  return (
    <div className="app" style={{ textAlign: 'center', marginTop: '10px' }}>
      <h1 className="title">DataDrip Test</h1>
      <hr />

      <h2 className="introduction">
        Please select your gender and upload a clear photo of your face :D
      </h2>

      <div className='gender-button'>
        <button
          onClick={() => setGender('mens')}
          className={gender === 'mens' ? 'selected-button' : 'unselected-button'}
        >Male</button>
        <button
          onClick={() => setGender('womens')}
          className={gender === 'womens' ? 'selected-button' : 'unselected-button'}
        >Female</button>
      </div>

      <Accept setFile={setFile} />
      {preview && (
        <div className="results">
          <h3>Preview:</h3>
          <img
            src={preview}
            alt="Uploaded preview"
            style={{ maxHeight: '250px', width: 'auto', marginTop: '10px' }}
          />
        </div>
      )}
      <br>
      </br>
      <button onClick={handleUpload} className="upload-button">Upload</button>

      {season && (
        <div className="results">
          <h2>Detected Season: {season}</h2>
          <h3>Recommended Palette:</h3>
          <div className="palette-grid">
            {palette.map(([colorName, hexValue], i) => (
              <div key={i} className="color-box">
                <div className="color-swatch" style={{ backgroundColor: hexValue }} />
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
      <br>
      </br>
      {images.top && images.bottom && images.shoes && (
      <div className="images">
        <img
          src={images.top.url}
          alt="Top"
          style={{ maxHeight: '300px', width: 'auto' }}
        />
        <img
          src={images.bottom.url}
          alt="Bottom"
          style={{ maxHeight: '300px', width: 'auto' }}
        />
        <img
          src={images.shoes.url}
          alt="Shoes"
          style={{ maxHeight: '300px', width: 'auto' }}
        />
      </div>

      )}


    </div>
  );
}

export default App;
