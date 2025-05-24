import React, { useState } from 'react';
import { RxCross2 } from 'react-icons/rx';
import toast from 'react-hot-toast';
import axios from 'axios';
import { BiSend } from "react-icons/bi";

const SendEmail = ({ open, setOpen, setEmails, emails }) => {
    const generateId = () => Math.random().toString(36).substring(2, 12);

    const getCurrentTime = () => {
        const now = new Date();
        return now.toTimeString().slice(0, 5);
    };

    const getCurrentDate = () => {
        const now = new Date();
        return `${String(now.getDate()).padStart(2, '0')}/${String(now.getMonth() + 1).padStart(2, '0')}/${now.getFullYear()}`;
    };

    const [formData, setFormData] = useState({
        threadId: generateId(),
        messageId: generateId(),
        from: "",
        to: "",
        subject: "",
        message: "",
        time: getCurrentTime(),
        date: getCurrentDate()
    });

    const [loading, setLoading] = useState(false);

    const changeHandler = (e) => {
        setFormData({ ...formData, [e.target.name]: e.target.value });
    };

    const submitHandler = async (e) => {
        e.preventDefault();

        try {
            const updatedData = {
                ...formData,
          
                time: getCurrentTime(),
                date: getCurrentDate(),
                messageId: generateId(),
                threadId: formData.threadId || generateId(),
                aiGenerated: false
            };

            const res = await axios.post("http://localhost:8080/api/v1/email/create", updatedData, {
                headers: { 'Content-Type': "application/json" },
                withCredentials: true
            });

            setEmails([...emails, res.data.email]);
            toast.success("Email sent successfully!");

            setFormData({
                threadId: generateId(),
                messageId: generateId(),
                from: "",
                to: "",
                subject: "",
                message: "",
                time: getCurrentTime(),
                date: getCurrentDate()
            });
            setOpen(false);
        } catch (error) {
            console.error(error);
            toast.error(error.response?.data?.message || "Failed to send email.");
        }
    };

    const generateAIEmail = async () => {
        setLoading(true);
        try {
            const res = await axios.post("http://localhost:8080/api/v1/email/generate-ai",
                { subject: formData.subject }, {
                headers: { 'Content-Type': "application/json" },
                withCredentials: true
            });

            setFormData({ ...formData, message: res.data.generatedMessage });
            toast.success("AI-generated email ready!");
        } catch (error) {
            console.error(error);
            toast.error("AI generation failed.");
        }
        setLoading(false);
    };

    return (
        <div className={`${open ? 'fixed inset-0 flex items-center justify-center bg-black bg-opacity-50 z-50' : 'hidden'}`}>
            <div className="bg-white max-w-2xl w-full mx-4 p-6 rounded-lg shadow-xl">
                <div className='flex items-center justify-between pb-4 border-b'>
                    <h1 className="text-lg font-semibold">New Message</h1>
                    <div onClick={() => setOpen(false)} className='p-2 rounded-full hover:bg-gray-200 cursor-pointer'>
                        <RxCross2 size="20px" />
                    </div>
                </div>

                <form onSubmit={submitHandler} className='flex flex-col gap-4 mt-4'>
  {/* From */}
  <div className="flex items-center gap-4">
  <label htmlFor="from" className="w-20 text-sm font-medium bg-gradient-to-r from-[#6936D6] to-[#152A65] bg-clip-text text-transparent">From</label>

    <input
      name="from"
      onChange={changeHandler}
      value={formData.from}
      type="email"
      placeholder='Enter sender email'
      className='flex-1 border rounded-md px-3 py-2 outline-none focus:ring-2 focus:ring-[#6936D6]'
      required
    />
  </div>

  {/* To */}
  <div className="flex items-center gap-4">
  <label htmlFor="from" className="w-20 text-sm font-medium bg-gradient-to-r from-[#6936D6] to-[#152A65] bg-clip-text text-transparent">To</label>

    <input
      name="to"
      onChange={changeHandler}
      value={formData.to}
      type="email"
      placeholder='Enter recipient email'
      className='flex-1 border rounded-md px-3 py-2 outline-none focus:ring-2 focus:ring-[#6936D6]'
      required
    />
  </div>

  {/* Subject */}
  <div className="flex items-center gap-4">
  <label htmlFor="from" className="w-20 text-sm font-medium bg-gradient-to-r from-[#6936D6] to-[#152A65] bg-clip-text text-transparent">Subject</label>

  <div className="flex items-center flex-1 border rounded-md px-3 py-2 bg-white focus-within:ring-2 ">
    <div className="w-6 h-6 min-w-[24px] min-h-[24px] bg-[#6936D6] rounded-full flex items-center justify-center mr-2">
      <img
src="https://creazilla-store.fra1.digitaloceanspaces.com/cliparts/3492595/purple-circle-100-clipart-xl.png"        alt="Icon"
        className="w-4 h-4"
      />
    </div>
    <input
      name="subject"
      onChange={changeHandler}
      value={formData.subject}
      type="text"
      placeholder='What will you write today?'
      className='flex-1 outline-none bg-transparent'
      required
    />
  </div>
</div>


  {/* Message */}
  <div className="flex flex-col">
  <label
    htmlFor="message"
    className="w-20 text-sm font-medium mb-2 bg-gradient-to-r from-[#6936D6] to-[#152A65] bg-clip-text text-transparent"
  >
    Message
  </label>

  <textarea
    name="message"
    onChange={changeHandler}
    value={formData.message}
    rows="8"
    placeholder="Write your message here..."
    className="border rounded-md px-3 py-2 outline-none focus:ring-2 focus:ring-[#6936D6]"
    required
  />
</div>


  {/* Buttons */}
  <div className="flex gap-3 mt-4">
  <button
  type="submit"
  className="flex items-center gap-2 rounded-full px-6 py-2 text-white font-medium transition duration-300 ease-in-out"
  style={{
    backgroundImage: 'linear-gradient(90deg, #6936D6 0%, #152A65 100%)'
  }}
>
<BiSend className="w-5 h-5 -rotate-45" />

  Send
</button>


    <button
      type="button"
      onClick={generateAIEmail}
      className="flex items-center gap-2 rounded-full px-6 py-2 text-white font-medium transition duration-300 ease-in-out"
      style={{
        backgroundImage: 'linear-gradient(90deg, #6936D6 0%, #152A65 100%)'
      }}
      disabled={loading}
    >
      <img
        src="https://gofloww.co/img/atom%20mail/vector-new%20.webp"
        alt="AI Logo"
        className="w-5 h-5"
      />
      {loading ? "Generating..." : "AI Generate"}
    </button>
  </div>
</form>

            </div>
        </div>
    );
};

export default SendEmail;
