import mongoose from "mongoose";

const emailSchema = new mongoose.Schema({
  threadId: {
    type: String,
    required: true,
  },
  messageId: {
    type: String,
    required: true,
  },
  from: {
    type: String,
    required: true,
  },
  to: {
    type: String,
    required: true,
  },
  subject: {
    type: String,
    required: true,
  },
  message: {
    type: String,
    required: true,
  },
  aiGenerated: {
    type: Boolean,
    default: false,
  },
  context: {
    type: String,
    default: "",
  },
  date: {
    type: String, // or Date, but you're sending as "dd/mm/yyyy"
    required: true,
  },
  time: {
    type: String, // "HH:mm" format
    required: true,
  }
}, { timestamps: true });

export const Email = mongoose.model("Email", emailSchema);
