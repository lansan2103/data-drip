import React from 'react';
import './Header.css';


function Header() {
    return (
        <header className = 'header'>
            <img src="logo.png" alt="DataDrip" className="logo" />
            <nav>
                <ul>
                    <a href="/">Take the Test</a>
                    <a href="/about">About</a>
                </ul>
            </nav>
        </header>
    );
}

export default Header;