import axios from 'axios';
import React, { useState } from 'react';
import toast from 'react-hot-toast';
import { useDispatch } from 'react-redux';
import { Link, useNavigate } from 'react-router-dom';
import { setAuthUser } from '../redux/appSlice';

const Login = () => {
  const [input, setInput] = useState({ email: '', password: '' });
  const [loading, setLoading] = useState(false);

  const dispatch = useDispatch();
  const navigate = useNavigate();

  const changeHandler = (e) => {
    setInput({ ...input, [e.target.name]: e.target.value });
  };

  const submitHandler = async (e) => {
    e.preventDefault();

    if (!input.email || !input.password) {
      toast.error("Please fill in all fields");
      return;
    }

    setLoading(true);
    try {
      const res = await axios.post(
        "http://localhost:8080/api/v1/user/login",
        input,
        {
          headers: { 'Content-Type': 'application/json' },
          withCredentials: true, // Send cookies with request
        }
      );

      if (res.data.success) {
        dispatch(setAuthUser(res.data.user)); // Update Redux state
        toast.success(res.data.message || "Login successful");
        navigate('/');
      }
    } catch (error) {
      console.error("Login error:", error);
      toast.error(error?.response?.data?.message || "Login failed. Try again.");
    }
    setLoading(false);
  };

  return (
    <div className='flex items-center justify-center w-screen h-screen bg-gray-100'>
      <form onSubmit={submitHandler} className='flex flex-col gap-4 bg-white p-6 w-[90%] max-w-md rounded-md shadow-lg'>
        <h1 className='font-bold text-2xl uppercase text-center'>Login</h1>
        <input
          onChange={changeHandler}
          value={input.email}
          name="email"
          type='email'
          placeholder='Email'
          className='border border-gray-400 rounded-md px-3 py-2'
          required
        />
        <input
          onChange={changeHandler}
          value={input.password}
          name="password"
          type='password'
          placeholder='Password'
          className='border border-gray-400 rounded-md px-3 py-2'
          required
        />
        <button
          type="submit"
          className={`bg-gray-800 p-2 text-white rounded-md transition-all duration-200 ${
            loading ? 'opacity-50 cursor-not-allowed' : 'hover:bg-gray-700'
          }`}
          disabled={loading}
        >
          {loading ? "Logging in..." : "Login"}
        </button>
        <p className='text-sm text-center'>
          Don't have an account?{' '}
          <Link to="/signup" className='text-blue-600 hover:underline'>Signup</Link>
        </p>
      </form>
    </div>
  );
};

export default Login;
