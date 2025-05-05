import React from "react";
import { Link } from "react-router-dom";

function Page1() {
  return (
    <div>
      <br />
      <br />
      <h1 className="introduction">This is an AI-powered fashion assistant that helps you create the perfect outfit for any occasion!</h1>
      <h1 className="introduction">Simply upload an image of a clothing item, and the program will analyze its style, color, and fit, then recommend complementary pieces from your wardrobe or suggest new ones to complete your look. </h1>
      <h1 className="introduction">Whether you're dressing for a formal event, a casual day out, or a business meeting, the app provides outfit suggestions tailored to the occasion.</h1>
      <h1 className="introduction">With real-time feedback on how well your outfit matches the event, you'll always step out in style with confidence!</h1>

      <br />
      <br />
      <br />
      <br />
      <br />
      <br />
      <br />
      <br />
      
      <Link to="/page1">
        <button className="nav-button" style={{marginLeft: '250px'}}>Go to Our Test!</button>
      </Link>

      <br />
      <br />
      
      {/* <p>
      Click on the button below
      </p> */}
      <Link to="/page2">
        <button className="nav-button" style={{marginLeft: '250px'}}>Go to About</button>
      </Link>


    <br />
    <br />
    <br />
    <br />
    <br />


    </div>

    
  );
}



export default Page1;
