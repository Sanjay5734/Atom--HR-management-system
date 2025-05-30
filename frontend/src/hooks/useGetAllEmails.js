import axios from "axios";
import { useEffect } from "react";
import { useDispatch, useSelector } from "react-redux";
import { setEmails } from "../redux/appSlice";

const useGetAllEmails = () => {
    const dispatch = useDispatch();
    const emails = useSelector(store => store.app.emails); // Correct usage

    useEffect(() => {
        const fetchEmails = async () => {
            try {
                const res = await axios.get("http://localhost:8080/api/v1/email/getallemails", {
                    withCredentials: true
                });
                dispatch(setEmails(res.data.emails));
            } catch (error) {
                console.error("Error fetching emails:", error);
            }
        };
        fetchEmails();
    }, [dispatch]); // ✅ Added `dispatch` to dependency array

    return emails; // ✅ Return emails for components to use
};

export default useGetAllEmails;
