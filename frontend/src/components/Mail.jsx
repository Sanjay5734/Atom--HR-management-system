import React from 'react';
import {
  IoMdArrowBack, IoMdMore
} from 'react-icons/io';
import {
  BiArchiveIn
} from "react-icons/bi";
import {
  MdDeleteOutline, MdKeyboardArrowLeft, MdKeyboardArrowRight,
  MdOutlineAddTask, MdOutlineDriveFileMove,
  MdOutlineMarkEmailUnread, MdOutlineReport, MdOutlineWatchLater
} from 'react-icons/md';
import { useSelector } from 'react-redux';
import { useNavigate, useParams } from 'react-router-dom';
import axios from 'axios';
import toast from 'react-hot-toast';

const Mail = () => {
  const navigate = useNavigate();
  const { selectedEmail } = useSelector(store => store.app);
  const params = useParams();

  const deleteHandler = async () => {
    try {
      const res = await axios.delete(`http://localhost:8080/api/v1/email/${params.id}`);
      toast.success(res.data.message);
      navigate("/");
    } catch (error) {
      console.error("Delete failed:", error);
      toast.error("Failed to delete email.");
    }
  };

  return (
    <div className='flex-1 bg-white rounded-xl mx-5 shadow-md overflow-hidden'>
      {/* Top action bar */}
      <div className='flex items-center justify-between px-4 py-2 border-b bg-white'>
        <div className='flex items-center gap-2 text-gray-700'>
          <div onClick={() => navigate("/")} className='p-2 rounded-full hover:bg-gray-200 cursor-pointer'>
            <IoMdArrowBack size={'20px'} />
          </div>
          <div className='p-2 rounded-full hover:bg-gray-200 cursor-pointer'>
            <BiArchiveIn size={'20px'} />
          </div>
          <div className='p-2 rounded-full hover:bg-gray-200 cursor-pointer'>
            <MdOutlineReport size={'20px'} />
          </div>
          <div onClick={deleteHandler} className='p-2 rounded-full hover:bg-gray-200 cursor-pointer'>
            <MdDeleteOutline size={'20px'} />
          </div>
          <div className='p-2 rounded-full hover:bg-gray-200 cursor-pointer'>
            <MdOutlineMarkEmailUnread size={'20px'} />
          </div>
          <div className='p-2 rounded-full hover:bg-gray-200 cursor-pointer'>
            <MdOutlineWatchLater size={'20px'} />
          </div>
          <div className='p-2 rounded-full hover:bg-gray-200 cursor-pointer'>
            <MdOutlineAddTask size={'20px'} />
          </div>
          <div className='p-2 rounded-full hover:bg-gray-200 cursor-pointer'>
            <MdOutlineDriveFileMove size={'20px'} />
          </div>
          <div className='p-2 rounded-full hover:bg-gray-200 cursor-pointer'>
            <IoMdMore size={'20px'} />
          </div>
        </div>
        <div className='flex items-center gap-2 text-sm text-gray-600'>
          <span>1 to 50</span>
          <MdKeyboardArrowLeft size="24px" className='cursor-pointer hover:text-blue-600' />
          <MdKeyboardArrowRight size="24px" className='cursor-pointer hover:text-blue-600' />
        </div>
      </div>

      {/* Email content */}
      <div className='h-[90vh] overflow-y-auto p-6 bg-gray-50'>
        {/* Subject */}
        <div className='flex justify-between items-start mb-6'>
          <div className='flex items-center gap-2 flex-wrap'>
            <h1 className='text-2xl font-bold bg-gradient-to-r from-[#6936D6] to-[#152A65] bg-clip-text text-transparent'>
              {selectedEmail?.subject}
            </h1>
            <span className='text-xs bg-blue-100 text-blue-600 px-2 py-0.5 rounded-md'>Inbox</span>
          </div>
          <p className='text-sm text-gray-400'>
            {selectedEmail?.time || new Date(selectedEmail?.createdAt).toLocaleString()}
          </p>
        </div>

        {/* From, To, Sent */}
        <div className='grid gap-2 text-sm mb-6'>
          <div>
            <span className='font-medium bg-gradient-to-r from-[#6936D6] to-[#152A65] bg-clip-text text-transparent'>
              From:
            </span>{' '}
            <span className='font-semibold text-gray-800'>{selectedEmail?.from || "Unknown sender"}</span>
          </div>
          <div>
            <span className='font-medium bg-gradient-to-r from-[#6936D6] to-[#152A65] bg-clip-text text-transparent'>
              To:
            </span>{' '}
            <span className='font-semibold text-gray-800'>{selectedEmail?.to}</span>
          </div>
          <div>
            <span className='font-medium bg-gradient-to-r from-[#6936D6] to-[#152A65] bg-clip-text text-transparent'>
              Sent:
            </span>{' '}
            <span className='text-gray-700'>{new Date(selectedEmail?.createdAt).toLocaleString()}</span>
          </div>
        </div>

        {/* Message Body */}
        <div className='p-6 rounded-xl border shadow-md bg-gradient-to-r from-[#6936D6] to-[#152A65] text-white whitespace-pre-line leading-relaxed'>
          {selectedEmail?.message}
        </div>
      </div>
    </div>
  );
};

export default Mail;
