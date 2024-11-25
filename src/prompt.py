from langchain.prompts import PromptTemplate

def create_prompt(prompt="""Context: {context} Question: {question} """):
    return PromptTemplate.from_template(prompt)