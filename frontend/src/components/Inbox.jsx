import React, { useState } from 'react';
import { MdCropSquare, MdInbox, MdKeyboardArrowLeft, MdKeyboardArrowRight } from 'react-icons/md';
import { FaCaretDown } from "react-icons/fa";
import { IoMdMore, IoMdRefresh } from 'react-icons/io';
import Emails from './Emails';

const mailType = [
  {
    icon: <MdInbox size={'20px'} />,
    text: "Primary"
  }
];

const Inbox = () => {
  const [selected, setSelected] = useState(0);

  return (
    <div className='flex-1 bg-white rounded-xl mx-5 shadow-md'>
      {/* Top control bar */}
      <div className='flex items-center justify-between px-4 py-3 border-b bg-gray-50 rounded-t-xl'>
        <div className='flex items-center gap-3'>
          <div className='flex items-center gap-1 px-2 py-1 rounded-md hover:bg-gray-200 cursor-pointer'>
            <MdCropSquare size={'20px'} />
            <FaCaretDown size={'16px'} />
          </div>
          <div className='p-2 rounded-full hover:bg-gray-200 cursor-pointer'>
            <IoMdRefresh size={'20px'} />
          </div>
          <div className='p-2 rounded-full hover:bg-gray-200 cursor-pointer'>
            <IoMdMore size={'20px'} />
          </div>
        </div>
        <div className='flex items-center gap-2 text-sm text-gray-700'>
          <span>1 to 50</span>
          <MdKeyboardArrowLeft size="24px" className='cursor-pointer hover:text-blue-600' />
          <MdKeyboardArrowRight size="24px" className='cursor-pointer hover:text-blue-600' />
        </div>
      </div>

      {/* Tabs */}
      <div className='flex items-center gap-1 border-b bg-white sticky top-0 z-10'>
        {
          mailType.map((item, index) => (
            <button
              key={index}
              onClick={() => setSelected(index)}
              className={`relative flex items-center gap-3 p-4 w-52 text-sm font-medium transition-colors ${
                selected === index
                  ? "text-blue-600"
                  : "text-gray-700 hover:text-blue-600"
              }`}
            >
              {item.icon}
              <span>{item.text}</span>
              {selected === index && (
                <span className="absolute bottom-0 left-0 w-full h-1 bg-blue-600 rounded-t-full transition-all"></span>
              )}
            </button>
          ))
        }
      </div>

      {/* Emails */}
      <div className='h-[85vh] overflow-y-auto px-4 py-3 bg-gray-50'>
        {/* Render Email List */}
        <Emails />
      </div>
    </div>
  );
};

export default Inbox;
