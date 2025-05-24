import mongoose from "mongoose";
import { Email } from "../models/email.model.js";

export const createEmail = async (req, res) => {
  try {
    console.log("Received data:", req.body);

    // Destructure expected fields
    const {
      threadId,
      messageId,
      from,
      to,
      subject,
      message,
      time,
      date,
      aiGenerated = false,
      context = ""  // optional context field
    } = req.body;

    // Validate required fields
    if (!threadId || !messageId || !from || !to || !subject || !message || !time || !date) {
      return res.status(400).json({ message: "All fields are required", success: false });
    }

    // Construct the object cleanly
    const newEmail = {
      threadId,
      messageId,
      from,
      to,
      subject,
      message,
      time,
      date,
      aiGenerated,
      context
    };

    // Save to DB
    const email = await Email.create(newEmail);

    return res.status(201).json({ email, success: true });
  } catch (error) {
    console.error("Error in createEmail:", error);
    return res.status(500).json({ message: "Server error", success: false });
  }
};

export const deleteEmail = async (req, res) => {
  try {
    const emailId = req.params.id;
    if (!emailId) {
      return res.status(400).json({ message: "Email ID is required", success: false });
    }

    const email = await Email.findByIdAndDelete(emailId);
    if (!email) {
      return res.status(404).json({ message: "Email not found", success: false });
    }

    return res.status(200).json({ message: "Email deleted successfully", success: true });
  } catch (error) {
    console.error("Error in deleteEmail:", error);
    return res.status(500).json({ message: "Server error", success: false });
  }
};

export const getAllEmails = async (req, res) => {
  try {
    const emails = await Email.find({}).sort({ createdAt: -1 });
    return res.status(200).json({ emails, success: true });
  } catch (error) {
    console.error("Failed to fetch emails:", error);
    return res.status(500).json({ message: "Failed to fetch emails.", success: false });
  }
};

export const generateAIEmail = async (req, res) => {
  try {
    const { subject } = req.body;

    if (!subject) {
      return res.status(400).json({ message: "Subject is required.", success: false });
    }

    const generatedMessage = `Dear Recipient,\n\nThis is an AI-generated email regarding "${subject}". Let me know your thoughts.\n\nBest regards,\nYour AI Assistant`;

    return res.status(200).json({ generatedMessage, success: true });
  } catch (error) {
    console.error("Error in generateAIEmail:", error);
    return res.status(500).json({ message: "AI email generation failed.", success: false });
  }
};
