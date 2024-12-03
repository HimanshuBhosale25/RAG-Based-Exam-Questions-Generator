from langchain.document_loaders import PyPDFLoader
from langchain_ollama import ChatOllama
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.schema import Document
from langchain.prompts import PromptTemplate
from langchain.chains.summarize import load_summarize_chain
from langchain_ollama import OllamaEmbeddings
from langchain.vectorstores import FAISS
from langchain.chains import RetrievalQA
from src.prompt import *

def file_processing(file_path):
    loader = PyPDFLoader(file_path)
    data = loader.load()

    question_gen = ""
    for page in data:
         question_gen += page.page_content

    text_splitter = RecursiveCharacterTextSplitter(chunk_size=100000000, chunk_overlap=100)
    splits = text_splitter.split_text(question_gen[:10000])
    documents = [Document(page_content=split) for split in splits]
    text_splitter1 = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
    document_answer_gen = text_splitter1.split_documents(
    documents
    )     

    return documents,document_answer_gen


def llm_pipeline(file_path):
     documents, document_answer_gen = file_processing(file_path)

     from langchain_ollama import ChatOllama

     llm = ChatOllama(
     model = "llama3.2:1b",
     temperature = 0.8,
     num_predict = 256,
     # other params ...
     )
    
     PROMPT_QUESTIONS = PromptTemplate(template=prompt_template, input_variables=['text'])
     REFINE_PROMPT_QUESTIONS = PromptTemplate(
     input_variables=["existing_answer", "text"],
     template=refine_template,
     )
     ques_gen_chain = load_summarize_chain(llm = llm, 
                                           chain_type = "refine", 
                                           verbose = True, 
                                           question_prompt=PROMPT_QUESTIONS, 
                                           refine_prompt=REFINE_PROMPT_QUESTIONS)
     
     ques = ques_gen_chain.invoke(documents)
     result = ques['output_text']
     embed = OllamaEmbeddings(
     model="llama3.2:1b"
      )
     
     vector_store = FAISS.from_documents(document_answer_gen, embed)

     llm_answer_gen =ChatOllama(
     model = "llama3.2:1b",
     temperature = 0.8,
     num_predict = 256,
     # other params ...
      )
     result_list = result.split("\n")
     result1 = result_list[2:12]


     answer_generation_chain = RetrievalQA.from_chain_type(llm=llm_answer_gen, 
                                               chain_type="stuff", 
                                               retriever=vector_store.as_retriever())
     
     for question in result1:
        print("Question: ", question)
        answer = answer_generation_chain.run(question)
        print("Answer: ", answer)
        print("\n")
        # Save answer to file
        with open("answers1.txt", "a") as f:
            f.write("Question: " + question + "\n")
            f.write("Answer: " + answer + "\n"+ "\n"+ "\n")
       
     return  answer_generation_chain,result1
