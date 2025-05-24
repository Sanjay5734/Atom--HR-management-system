# prompts.py

# --- RAG Decision Prompts ---
RAG_EMAIL_REQD_PROMPT = """
Carefully analyze the user's latest query and the conversation history. Decide if retrieving **additional specific past emails** (beyond the immediate thread history, which might be provided separately) is **essential** to fulfill the user's request accurately.

**Decision Criteria:** Answer 'yes' ONLY IF the query explicitly asks for, or clearly implies the need for, information likely contained *only* in past email conversations. Consider these triggers:
*   Direct requests to find/recall specific emails ("Find email from...", "What did [person] say about [topic] in email?", "Search emails for...").
*   References to specific past dates, times, or events where details were likely communicated via email ("action items from last week's meeting email", "details announced around the 15th").
*   Requests to recall specific facts, figures, decisions, or attachments mentioned in previous email exchanges ("confirm the price we emailed about", "find the attachment Bob sent").
*   Follow-ups that implicitly require context from *other* email threads not currently visible.

Answer 'no' IF:
*   The query is a simple greeting, closing, or acknowledgement ("hi", "thanks", "okay").
*   The query asks to draft new content without needing specific details *from past emails* (e.g., "Draft email saying I'm OOO"). Drafting a *reply* might use thread history, but doesn't automatically need *other* email RAG.
*   The query asks for clarification or modification of the *current* assistant response ("make it shorter", "explain that").
*   The query can likely be answered using only the provided conversation history or general knowledge.

**Few-Shot Examples:**

1.  History: User asks about Project Zephyr status.
    Query: "Find the last email update Maria sent about Project Zephyr."
    Decision: yes

2.  History: AI drafted an email to a client.
    Query: "Okay, looks good, send it."
    Decision: no

3.  History: Discussion about upcoming Q4 planning.
    Query: "Remind me what budget figures were discussed in the emails last month for Q4?"
    Decision: yes

4.  History: User received an email about a required training.
    Query: "Draft a polite email asking to be excused from the training mentioned."
    Decision: no (Requires thread history maybe, but not searching *other* past emails for info)

5.  History: User asks general question about company holidays.
    Query: "How is the holiday schedule communicated usually?"
    Decision: no (This might need *document* RAG, not email RAG).

6.  History: None.
    Query: "hi"
    Decision: no

**Analysis:**

Conversation History:
{chat_history_str}

User Query: {user_query}

**Is searching past emails essential? (yes/no):**"""


RAG_DOC_REQD_PROMPT = """
Carefully analyze the user's latest query and the conversation history. Decide if retrieving relevant **company documents** (like policies, product specifications, FAQs, procedures, guides, templates) is **essential** to fulfill the user's request accurately.

**Decision Criteria:** Answer 'yes' ONLY IF the query explicitly asks for, or clearly implies the need for, information typically found in official company documentation. Consider these triggers:
*   Questions about specific company policies, rules, or guidelines ("What is the policy on...", "Are we allowed to...").
*   Requests for official procedures or step-by-step instructions ("How do I submit...", "What's the process for...").
*   Inquiries about specific product details, technical specifications, or features ("specs for product X", "user guide for software Y").
*   Requests for standard company templates, forms, or resources ("find the template for...", "where is the official org chart?").
*   Questions requiring factual, verifiable information likely documented internally (e.g., office locations, official contact lists).

Answer 'no' IF:
*   The query is conversational or a simple acknowledgement.
*   The query is about drafting emails or managing email content (unless the draft requires specific info *from a document*).
*   The query asks for information likely found in *emails* (e.g., specific past discussions, decisions between individuals).
*   The query can be answered using the provided conversation history or general knowledge.

**Few-Shot Examples:**

1.  History: User is planning a business trip.
    Query: "What is the company's policy regarding travel expense reimbursement?"
    Decision: yes

2.  History: Discussing a new software feature rollout.
    Query: "Where can I find the user guide documentation for this new feature?"
    Decision: yes

3.  History: User received an email from HR about benefits enrollment.
    Query: "Can you draft a reply asking for clarification on the deadline mentioned in the email?"
    Decision: no (This is about email drafting/replying, not document lookup).

4.  History: General chat about workload.
    Query: "How do I request vacation time?"
    Decision: yes

5.  History: AI provided specs for Product A.
    Query: "Thanks, that's helpful."
    Decision: no

6.  History: User asks about a meeting mentioned in an email.
    Query: "Who was invited according to that meeting email?"
    Decision: no (This needs *email* RAG, not document RAG).

**Analysis:**

Conversation History:
{chat_history_str}

User Query: {user_query}

**Is searching company documents essential? (yes/no):**"""


# --- Query Generation Prompts ---

# prompts.py

EMAIL_QUERY_GENERATION_PROMPT = """
Your task is to generate a concise and effective search query to find relevant **past emails** based on the user's request and conversation history. The query should maximize the chance of retrieving the *specific* email(s) containing the needed information.

**Analysis Steps:**
1.  **Identify Core Need:** What specific information, decision, attachment, or confirmation is the user *actually* looking for in past emails?
2.  **Extract Key Entities:** Identify crucial names (senders, recipients, mentioned people), project names, client names, or specific keywords central to the request.
3.  **Pinpoint Time References:** Extract any mentioned dates, date ranges (e.g., "last week", "in October", "around the 15th"), or references to specific events (e.g., "after the Q3 meeting").
4.  **Focus on Specificity:** Prioritize the most unique and identifying terms from the user's query and history. Avoid overly generic terms if specific ones are available.
5.  **Synthesize the Query:** Combine the most critical extracted elements into a natural language search query. Focus on keywords and concepts, not full sentences unless necessary to capture nuance.

**Example Generation:**

*   User Query: "Find the email Maria sent last Tuesday about the final Project Zephyr budget figures."
    *   *Analysis:* Need='final budget figures', Entities='Maria', 'Project Zephyr', Time='last Tuesday'.
    *   *Generated Query:* "Maria Project Zephyr final budget email last Tuesday"

*   User Query: "What was the decision regarding the client demo mentioned in emails around the start of the month?"
    *   *Analysis:* Need='decision', Topic='client demo', Time='start of month'. (History might clarify which client if multiple).
    *   *Generated Query:* "client demo decision email start of month"

*   User Query: "I need the presentation attachment from the onboarding email thread."
    *   *Analysis:* Need='presentation attachment', Topic='onboarding'.
    *   *Generated Query:* "onboarding email presentation attachment"

**Inputs:**

Conversation History:
{chat_history_str}

User Query: {user_query}

**Optimized Search Query for Past Emails:**"""

# prompts.py

DOC_QUERY_GENERATION_PROMPT = """
Your task is to generate a concise and effective search query to find relevant **company documents** (policies, guides, specs, templates, FAQs) based on the user's request and conversation history. The query should target the document most likely to contain the official information sought.

**Analysis Steps:**
1.  **Identify Core Need:** What specific policy, procedure, technical detail, template, or official information is the user looking for?
2.  **Extract Key Terms:** Identify official policy names (e.g., "Travel and Expense Policy"), product names/codes (e.g., "X1 Processor"), specific procedure types (e.g., "expense submission", "vacation request"), document types (e.g., "user guide", "FAQ", "template"), or keywords central to the topic.
3.  **Use Official Language:** If known, prioritize official terminology used within the company for the policy, product, or process.
4.  **Focus on Document Content:** Frame the query around the likely *content* or *title* of the target document.
5.  **Synthesize the Query:** Combine the most relevant and specific terms into a keyword-focused search query.

**Example Generation:**

*   User Query: "What is the official process for requesting parental leave?"
    *   *Analysis:* Need='process', Topic='parental leave'. Official term might be 'Parental Leave Policy'.
    *   *Generated Query:* "parental leave policy procedure" or "how to request parental leave"

*   User Query: "I need the technical specifications document for the new 'Aurora' software release."
    *   *Analysis:* Need='technical specifications', Entity='Aurora software'.
    *   *Generated Query:* "Aurora software technical specifications" or "Aurora release specs document"

*   User Query: "Where can I find the standard template for project kickoff presentations?"
    *   *Analysis:* Need='template', Topic='project kickoff presentation'.
    *   *Generated Query:* "project kickoff presentation template"

*   User Query: "What are the guidelines for using the company VPN when traveling internationally?"
    *   *Analysis:* Need='guidelines', Topic='VPN usage international travel'. Policy might be 'Remote Access Policy' or 'VPN Usage Guide'.
    *   *Generated Query:* "VPN international travel guidelines" or "remote access policy VPN usage"

**Inputs:**

Conversation History:
{chat_history_str}

User Query: {user_query}

**Optimized Search Query for Company Documents:**"""


# --- Decide the response type prompt ---
RESPONSE_TYPE_PROMPT = """
Analyze the user's latest query and the conversation history. Determine if the user is asking for an email to be drafted, asking a question that requires a formal email-style response, OR if it's a simple greeting, follow-up question, clarification, or casual chat message.

Consider the user's intent. Are they giving instructions to write something ("Draft an email...", "Write a reply saying...", "Ask them about...")? Or are they asking a question directly to you, the assistant ("What documents did you find?", "Can you make it shorter?", "hi")?

Conversation History:
{chat_history_str}

User Query: {user_query}

Respond with ONLY 'generate_email' if an email body needs to be drafted.
Respond with ONLY 'generate_chat' if a direct, conversational response is appropriate.

Response Type Decision:"""


# --- Email Writer Prompts ---

EMAIL_WRITER_SYSTEM_PROMPT = """You are a specialized AI assistant focused *solely* on drafting the **body text** of professional emails. Your primary function is to generate content suitable for the main part of an email message.

**Core Instructions:**
1.  **Generate ONLY Email Body Content:** Your output MUST be formatted as the body of an email. Start directly with the main message.
2.  **STRICTLY OMIT:** Do NOT include any greetings (e.g., "Hi [Name],", "Dear Team,"), opening pleasantries (e.g., "Hope you are doing well,"), or closing remarks (e.g., "Best regards,", "Thanks,"). Your response begins with the first sentence of the actual message content and ends with the last.
3.  **Always Produce Email Format:** Even if the user's request seems conversational (like "okay" or "thanks") or lacks detail, you MUST still generate text formatted as a minimal, professional email body.
4.  **Context is Key:** Base your response on the user's request (`user_query`) and synthesize information from the `Current Email Thread History`, `Relevant Retrieved Past Emails`, and `Relevant Retrieved Company Documents` provided in the context.
5.  **Professional Tone:** Maintain a clear, concise, and professional tone appropriate for workplace communication.
6.  **Handle Ambiguity Professionally:** If the user's request is unclear or insufficient context is available to draft a meaningful reply, generate a *polite placeholder body* asking for clarification or stating the limitation *within the email body format*. Examples:
    *   "Could you please provide more specific details regarding the training session?"
    *   "To follow up effectively, could you clarify which aspect of the report you'd like me to focus on?"
    *   "I understand you'd like an update, but I need more context about the specific project mentioned."
7.  **User Identity:** The user's email is {user_email}. This is for your context only and should generally not be repeated in the generated body.

**Output Format Reminder:** Your entire output will be placed directly into an email body. Do not add anything extra before or after the core message content."""

# This template will be formatted and passed as the *last* HumanMessage to the writer
EMAIL_WRITER_USER_TEMPLATE = """
Based on my request and the provided context below, generate the appropriate email body text. Follow the system instructions precisely (body only, professional format).

## My Request:
{user_query}

## Context:

### Current Email Thread History:
{thread_history}

### Relevant Retrieved Past Emails:
{retrieved_emails}

### Relevant Retrieved Company Documents:
{retrieved_docs}

---
Email Body Output:
"""


#  --- Simple chat agent prompt ---
CHAT_AGENT_SYSTEM_PROMPT = """You are a helpful assistant. Respond concisely and conversationally to the user's message, using the provided context if relevant.
If no specific context is needed, just provide a natural chat response."""

CHAT_AGENT_USER_TEMPLATE = """
Context:
{context_str}

User Query:
{user_query}

Your Conversational Response:"""
