import {useState} from 'react';
import React, {Component} from 'react';
import './App.css';
import {useDropzone" from 'react-dropzone';}
/*import axios from 'axios';

console.log("App component loaded");
      <button onClick={this.fileUploadHandler}>Upload</button>
class App extends Component{
  state = {
    selectedFile: null
  }

  fileSelectedHandler = event => {
    console.log(event.target.files(0));
  }
}
fileUploadHandler = () => {
  axios.post('')
}*/
function App() {
const [display, setDisplay] = useState(0);
function addNum(){
  setDisplay(display+1);
}  
function subNum(){
  setDisplay(display-1);
}

useDrop({
  accept: {
    'image/png': ['.jpg']
    'text/html':['.html','.htm']
  }
})
  return (
    <div className = 'app'>
      <div className = 'add'>
        <button onClick = {addNum}>+</button>
      </div>
      <h1 className = 'header'>DataDrip!</h1>
      <h1> Welcome to DataDrip!</h1>
      
      
      <h2 className = 'subheader'> Please insert a .jpg photo of your face in natural lighting from shoulders up</h2>
      <input type="file"></input>
            <button onClick>Upload</button>
      </div>

  );
}

export default App;
