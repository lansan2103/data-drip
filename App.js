import React from "react";
import './App.css';
// import { Button } from "@/components/ui/button";

export default function HomePage() {
  return (
    
    <div className="min-h-screen flex flex-col">
      {/* Navbar */}
      <nav className="bg-gray-900 text-white p-4 flex justify-between items-center shadow-md">
        <h1 className="text-xl font-bold">DataDrip</h1>
        <div>
          {/* <Button variant="outline" className="text-white border-white">Get Started</Button> */}
        </div>
      </nav>
      
      {/* Hero Section */}
      <main className="flex-1 flex flex-col items-center justify-center text-center p-10">
        <h2 className="text-4xl font-bold mb-4">pink</h2>
        <p className="text-lg text-gray-600 mb-6">HIIII</p>
        {/* <Button className="px-6 py-3 text-lg">Explore</Button> */}

        {/* Image */}
        <img src="/austin.jpg" alt="LeBron Image" className="w-64 h-auto rounded-lg shadow-lg" />

      </main>
      
      {/* Footer */}
      {/* <footer className="bg-gray-900 text-white text-center p-4 mt-auto">
        <p>&copy; {new Date().getFullYear()} My Website. All rights reserved.</p>
      </footer> */}
    </div>
  );
}

{/* <img src="lebron2.png" alt="LeBron Image"> */}
