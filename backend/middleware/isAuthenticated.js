import jwt from "jsonwebtoken";
import { User } from "../models/user.model.js";

const isAuthenticated = async (req, res, next) => {
    try {
        const token = req.cookies.token;  // Ensure you're using `cookie-parser`

        if (!token) {
            return res.status(401).json({ message: "No token, authorization denied" });
        }

        const decoded = jwt.verify(token, process.env.SECRET_KEY);
        req.user = await User.findById(decoded.userId).select("-password"); // ✅ Set req.user

        if (!req.user) {
            return res.status(401).json({ message: "User not found, authorization denied" });
        }

        next();
    } catch (error) {
        console.error(error);
        return res.status(401).json({ message: "Invalid token" });
    }
};

export default isAuthenticated;
