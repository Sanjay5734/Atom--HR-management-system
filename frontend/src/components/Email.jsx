import React, { useState } from 'react';
import { MdCropSquare, MdOutlineStarBorder, MdStar, MdAccessTime, MdSubject } from 'react-icons/md';
import { useDispatch } from 'react-redux';
import { useNavigate } from 'react-router-dom';
import { setSelectedEmail } from '../redux/appSlice';

const Email = ({ email }) => {
  const navigate = useNavigate();
  const dispatch = useDispatch();
  const [isStarred, setIsStarred] = useState(false);

  const openMail = () => {
    dispatch(setSelectedEmail(email));
    navigate(`/mail/${email._id}`);
  };

  const toggleStar = (e) => {
    e.stopPropagation(); // Prevent triggering openMail()
    setIsStarred(!isStarred);
  };

  return (
    <div
      onClick={openMail}
      role="button"
      tabIndex={0}
      onKeyDown={(e) => e.key === 'Enter' && openMail()}
      className="flex items-center justify-between px-4 py-3 bg-white hover:bg-gray-50 border border-gray-200 rounded-xl transition-shadow hover:shadow-md cursor-pointer"
    >
      <div className="flex items-center gap-3 text-gray-500">
        <MdCropSquare size={20} />
        <button onClick={toggleStar}>
          {isStarred ? (
            <MdStar size={20} className="text-yellow-400" />
          ) : (
            <MdOutlineStarBorder size={20} />
          )}
        </button>
      </div>

      <div className="flex-1 mx-4 min-w-0">
        <div className="flex items-center gap-2 text-gray-700 font-semibold truncate">
          <MdSubject className="text-[#6936D6]" size={18} />
          <h1 className="bg-gradient-to-r from-[#6936D6] to-[#152A65] bg-clip-text text-transparent truncate">
            {email?.subject}
          </h1>
        </div>
        <p className="text-sm text-gray-600 truncate">{email?.body}</p>
      </div>

      <div className="flex items-center gap-1 text-xs text-gray-400 whitespace-nowrap">
        <MdAccessTime size={16} />
        {new Date(email?.createdAt).toLocaleString()}
      </div>
    </div>
  );
};

export default Email;
