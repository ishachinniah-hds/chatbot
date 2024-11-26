from langchain.prompts import PromptTemplate

def create_prompt(prompt):
    """
    Generates the prompt template
    """
    return PromptTemplate.from_template(prompt)