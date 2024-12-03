prompt_template = """
You are an expert at creating questions based on materials and documentation.
Your goal is to prepare people for their exam.
You do this by asking questions about the text below:

------------
{text}
------------

Create 10 single line questions that will prepare for tests and do not even add your response.
The answers to these questions should be within the given context.
Do not even say anything from your side
Do not give multiple choice questions.
Do not add extra new line characters.
I'm going to split these questions with python so i can get a list of questions.
Make sure not to lose any important information.

QUESTIONS:
"""

refine_template = ("""
You are an expert at creating practice questions based on  material and documentation.
Your goal is to help people prepare for test.
We have received some practice questions to a certain extent: {existing_answer}.
We have the option to refine the existing questions or add new ones.
(only if necessary) with some more context below.
------------
{text}
------------

Given the new context, refine the original questions in English.
If the context is not helpful, please provide the original questions.
QUESTIONS:
"""
)