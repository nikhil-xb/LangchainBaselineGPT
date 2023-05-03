import json
import os
from pathlib import Path
from langchain.text_splitter import RecursiveCharacterTextSplitter
import faiss
from langchain.vectorstores import FAISS
from langchain.embeddings import OpenAIEmbeddings
import pickle
import openai
from langchain import OpenAI, LLMChain
from langchain.prompts import Prompt
import tiktoken

os.environ['OPENAI_API_KEY']= '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'
tokenizer= tiktoken.get_encoding('cl100k_base')
def tiktoken_len(text):
    tokens= tokenizer.encode(text, disallowed_special= ())
    return len(tokens)
def train():
    # Access the files
    trainData=  os.listdir('../train/')
    data= []
    for train in trainData:
        if train.endswith('.txt'):
            train= os.path.join('../train', train)
            with open(train) as file:
                print(f"Add {train} to the dataset ")
                data.append(file.read()) 
            file.close()

    # Token Limit solved using Langchain
    textSplit= RecursiveCharacterTextSplitter(chunk_size= 400,chunk_overlap=20, length_function= tiktoken_len, separators=['\n\n','\n', ' ',''])
    docs= []
    for sets in data:
        docs.extend(textSplit.split_text(sets))

    store=  FAISS.from_texts(docs, OpenAIEmbeddings())
    faiss.write_index(store.index, "training.index")
    store.index= None

    with open("faiss.pkl", "wb") as f:
        pickle.dump(store, f)
# To create the pkl file, uncomment the below and run engine.py
#train()

class Chat:

    def onMessage(selCf, llmchain, store, question, history):
            docs= store.similarity_search(question)
            context= []
            for i, doc in enumerate(docs):
                context.append(f"Context {i}:\n{doc.page_content}")
                answer= llmchain.predict(question= question, context= "\n\n".join(context), history= history)
            return answer
    def lets_prompt(self,prompt_, history):
        index= faiss.read_index('training.index')
        with open("faiss.pkl", "rb") as file:
            store= pickle.load(file)
        file.close()
        store.index= index

        with open("prompts.txt", "r") as file:
            promptTemplate= file.read()
        file.close()
        
        prompt= Prompt(template= promptTemplate, input_variables= ["history", "context", "question"])
        llmchain= LLMChain(prompt= prompt, llm= OpenAI(temperature= 0.3))

        answer= self.onMessage(llmchain, store, prompt_, history)
        history.append(f"User: {prompt_}")
        history.append(f"NikhilGPT: {answer}")
        return answer, history
        

        

