import React from 'react';
import { Link } from 'react-router-dom';
import './Header.css';
import logo from './datadriplogo.png'

function Header() {
    return (
        <header className = 'header'>
            <div className='logo-container'>
                <img src={logo} alt="DataDrip" className="logo"/>
                <Link to='/' className='logo-link'>DataDrip</Link> 
            </div>
            <div className='nav-container'>

                <Link to='/' className='link'>About</Link>
                <Link to='/test'className='link'>Take the Test</Link>
            </div>

        </header> 
    );
}


export default Header;