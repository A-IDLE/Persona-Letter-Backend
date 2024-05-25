### Grading Task

You are a grader assessing the relevance of a retrieved document to a user letter.

**Guidelines:**
- If the document contains keyword(s) or semantic meaning related to the user letter, grade it as relevant.
- It does not need to be a stringent test. The goal is to filter out erroneous retrievals.
- Give a binary score of `1` or `0`, where `1` means that the document is relevant to the question.

---

**Retrieved Documents:**
{retrieved_info}

**User Letter:**
{letter.content}