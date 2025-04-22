import React from "react";
import { Link } from "react-router-dom";

function Page1() {
  return (
    <div>
      <p>
        First page!
        <br />
        Click on the button below
      </p>
      <Link to="/page2">
        <button className="nav-button">Go to About</button>
      </Link>
    </div>
  );
}



export default Page1;
