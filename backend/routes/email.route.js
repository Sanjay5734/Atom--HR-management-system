import express from "express"; 
import {
  createEmail,
  deleteEmail,
  getAllEmails,
  generateAIEmail
} from "../controllers/email.controller.js";

const router = express.Router();

router.post("/create", createEmail);
router.delete("/:id", deleteEmail);
router.get("/getallemails", getAllEmails);
router.post("/generate-ai", generateAIEmail);

export default router;
