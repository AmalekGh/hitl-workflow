class Prompts:
    def __init__(self):
        pass
    
    def get_prompt(self, context: str, query: str):
        prompt = f"""
Context information is belowe. It represents parts of a research paper.
----------------------------------------------------------------------
{context}
--------------------------------------------------------------------
Given the context information above about the research paper and no prior knowledge:
You willl extract the values corresponding to the list of properties given in the query.
Your output should always be like this: <extraction><key>PROPERTies</key><value>VALUE</value></extraction>.
If you DO NOT find the value in the content, then your output should be like this: <extraction><key>PROPERTies</key><value>UNKNOWN</value></extraction>.
---------------------------------------------------------------------------
Query: {query}

Answer: \
"""
        return prompt
    
    def get_prompt_2(self, context: str, query:str):
        prompt = f"""INSTRUCTIONS:
Answer the users QUESTION using the DOCUMENT text above and no prior knowledge.
Your answer should ONLY consist of the extracted information, and no further explanation.
----------------------------------------------
DOCUMENT: 
    {context}
----------------------------------------------
QUESTION:
    {query}      
"""
        return prompt
        

    