prompt_template = """
You are an expert at creating questions based on materials and documentation.
Your goal is to prepare people for their exam.
You do this by asking questions about the text below:

------------
{text}
------------

Create 10 single line questions that will prepare for tests.
Do not give multiple choice questions.
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
