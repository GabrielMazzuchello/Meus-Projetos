import React from 'react'
import logoSpotiy from '../assets/logo/spotify-logo.png';

const Header = () => {
  return (
    <div className="header">
        <img src={logoSpotiy} alt=""/>
        
        <a className='header__link' href="/">
            <h1>Spotify</h1>
        </a>
    </div>
  );
}

export default Header