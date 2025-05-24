import React, { useState } from 'react';
import { LuPencil } from "react-icons/lu";
import { MdInbox, MdContacts, MdSettings, MdInfo } from "react-icons/md";
import { useNavigate } from 'react-router-dom';
// import SendEmail from './SendEmail';

const sidebarItems = [
    { icon: <MdInbox size={'20px'} />, text: "Mails", path: "/" },
    { icon: <MdContacts size={'20px'} />, text: "Contacts", path: "/contacts" },

    { icon: <MdSettings size={'20px'} />, text: "Settings", path: "/settings" },
    { icon: <MdInfo size={'20px'} />, text: "About", path: "/about" }
];

const Sidebar = () => {
    const navigate = useNavigate();
    const [open, setOpen] = useState(false);
    const [emails, setEmails] = useState([]);

    return (
        <>
            <div 
                className='w-[15%] min-h-screen text-white' 
                style={{ backgroundImage: "linear-gradient(90deg, #6936D6 0%, #152A65 100%)" }}
            >
                <div className='p-3'>
                <button
  onClick={() => setOpen(true)}
  className="flex items-center gap-2 w-[82%] mx-auto p-4 rounded-2xl shadow-custom-box-shadow hover:shadow-secondary-btn ease-in duration-300 bg-white"
>
  <LuPencil size="25px" color="#6936D6" />
  <span className="text-[#6936D6] font-semibold">Compose</span>
</button>

                </div>
                <div className=''>
                    {sidebarItems.map((item, index) => (
                        <div 
                            key={index}
                            onClick={() => navigate(item.path)}
                            className='flex items-center pl-6 py-2 rounded-r-full gap-4 my-2 hover:cursor-pointer hover:bg-[#ffffff30]'
                        >
                            {item.icon}
                            <p>{item.text}</p>
                        </div>
                    ))}
                </div>
            </div>
            <SendEmail open={open} setOpen={setOpen} emails={emails} setEmails={setEmails} />
        </>
    );
};

export default Sidebar;
