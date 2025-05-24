import React, { useEffect, useState } from 'react';
import { RxHamburgerMenu } from "react-icons/rx";
import { IoIosSearch, IoIosSettings } from "react-icons/io";
import { TbGridDots } from "react-icons/tb";
import Avatar from 'react-avatar';
import { useDispatch } from 'react-redux';
import { setSearchText } from '../redux/appSlice';

const Navbar = () => {
    const [text, setText] = useState("");
    const dispatch = useDispatch();

    useEffect(() => {
        dispatch(setSearchText(text));
    }, [text]);

    return (
        <div 
            className='flex items-center justify-between w-full h-16 px-6 '
            style={{ backgroundImage: 'linear-gradient(90deg, #6936D6 0%, #152A65 100%)' }}
        >
            <div className='flex items-center gap-10 text-white'>
                <div className='flex items-center gap-2'>
                    <div className='p-3 hover:bg-[#7c5ed1] rounded-full cursor-pointer'>
                        <RxHamburgerMenu />
                    </div>
                    <a className="navbar-brand self-center">
                        <img className="w-29 h-10" src="https://gofloww.co/img/atom%20mail/Group%2052.webp" alt="logo" />
                    </a>
                    <a>atomai</a>
                </div>
            </div>

            <div className='w-[40%]'>
                <div className='flex items-center bg-white px-3 py-2 rounded-full'>
                    <IoIosSearch size={'24px'} className='text-gray-700' />
                    <input
                        type="text"
                        value={text}
                        onChange={(e) => setText(e.target.value)}
                        placeholder='Search Mail'
                        className='rounded-full w-full bg-transparent outline-none px-2 text-black'
                    />
                </div>
            </div>

            <div className='flex items-center gap-3 text-white'>
                <div className='p-2 rounded-full hover:bg-[#7c5ed1] cursor-pointer'>
                    <IoIosSettings size={'24px'} />
                </div>
                <div className='p-2 rounded-full hover:bg-[#7c5ed1] cursor-pointer'>
                    <TbGridDots size={'24px'} />
                </div>
                <Avatar name="User" size="40" round={true} />
            </div>
        </div>
    );
};

export default Navbar;
