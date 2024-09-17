import React from 'react';

function MyButton() {
  const handleClick = () => {
    alert('Button clicked!');
  };

  return (
    <button onClick={handleClick}>
      Run Script 1!
    </button>
  );
}

export default MyButton;