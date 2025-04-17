import React from 'react';
import { Link } from 'react-router-dom';
import './Header.css';


function Header() {
    return (
        <header className = 'header'>
            <img src="logo.png" alt="DataDrip" className="logo"/>
            <Link to='/'>DataDrip</Link> 
                {/* until i find out how to be able to click the DataDrip pic */}
                
            <nav>
                <ul>
                        <Link to='/page1'>Take the Test</Link>
                    <br />
                        <Link to='/page2'>About</Link>
                </ul>
            </nav>
        </header>
    );
}


export default Header;