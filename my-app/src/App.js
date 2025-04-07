import {useState} from 'react';
import './App.css';

console.log("App component loaded");

function App() {
const [display, setDisplay] = useState(0);
function addNum(){
  setDisplay(display+1);
}  
function subNum(){
  setDisplay(display-1);
}
  return (
    <div className = 'app'>
      <div className = 'add'>
        <button onClick = {addNum}>+</button>
      </div>
      <h1 className = 'header'>DataDrip!</h1>

      <div className = 'subtract'>
        <button onClick = {subNum}>-</button>
      </div>
    </div>

  );
}

export default App;
