import { createBrowserRouter, RouterProvider } from 'react-router-dom'
import './App.css'
import Inbox from './components/Inbox'
import Navbar from './components/Navbar'
import Sidebar from './components/Sidebar'
import Body from './components/Body'
import Mail from './components/Mail'
import SendEmail from './components/SendEmail'
import Login from './components/Login'
import Signup from './components/Signup'
import { Toaster } from 'react-hot-toast'
import Contact from './components/contacts'
const appRouter = createBrowserRouter([
  {
    path: "/",
    element: <Body />,
    children: [
      {
        path: "/",
        element: <Inbox />
      },
      {
        path: "/contacts",
        element: <Contact />
      },
      {
        path: "/mail/:id",
        element: <Mail />
      },
      {
        path: "/compose",
        element: <SendEmail />
      }
    ]
  },
  {
    path:"/login",
    element:<Login/>
  },
  {
    path:"/signup",
    element:<Signup/>
  }
])

function App() {
  return (
    <div className='bg-[#F6F8FC] h-screen'>
      <RouterProvider router={appRouter} />
      <Toaster />
    </div>
  )
}

export default App;
