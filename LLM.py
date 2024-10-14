class LLM(object):
    def __init__(self, api_key, model, model_string):
        self.api_key = api_key
        self.model = model
        self.model_string = model_string
        self.context = "You are an undergraduate Operating Systems student who is going to be taking an exam. You are only to answer with the lowercase letter representing the correct answer. Do not include any other information or explanation in your response. Answer all questions on the page. The page will be inputted as a"
    
    def call_model(self, file, is_text):
        # use the correct syntax for each type of model (claude, gemini, llama, openai)
        if self.model_string == "claude":
            