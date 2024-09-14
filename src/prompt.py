from langchain import hub

def prompt_template():
    prompt = hub.pull("hwchase17/react")
    return prompt