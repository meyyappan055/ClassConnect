import React from 'react';

const Card = ({ icon, title, text }) => {
  return (
    <div className="flex flex-col bg-black text-white p-6 rounded-xl shadow-md border border-gray-800 max-w-lg min-h-[176px] m-4">
      <div className="flex-shrink-0 text-white mb-2 text-3xl">{icon}</div>
      <h3 className="flex-shrink-0 font-semibold text-lg mb-2">{title}</h3>
      <p className="text-gray-400 text-sm">{text}</p>
    </div>
  );
};

export default Card;
