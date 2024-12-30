import React from 'react';

const Card = ({ icon, title, text }) => {
  return (
    <div className="flex flex-col bg-black text-white p-6 rounded-xl shadow-md border-1 max-w-lg h-44 m-4">

      <div className="text-white mb-4 text-3xl">{icon}</div>
      <h3 className="font-semibold text-lg mb-2">{title}</h3>
      <p className="text-gray-400 text-sm">{text}</p>
      
    </div>
  );
};

export default Card;
