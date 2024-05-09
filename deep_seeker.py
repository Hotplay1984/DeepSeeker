from openai import OpenAI
import os
from IPython.core.magic import register_cell_magic


def get_api_key():
    api_key = os.getenv('DeepSeekAPI_KEY')
    if not api_key:
        raise EnvironmentError("API Key not found. Please set it in your environment variables.")
    return api_key


def ask(msg, model='c', print_on_screen=True):
    base_url="https://api.deepseek.com"
    api_key = get_api_key()
    client = OpenAI(api_key=api_key, base_url=base_url)
    
    model_mapping = {'c': 'deepseek-chat', 'p': 'deepseek-coder'}
    
    try:
        res = client.chat.completions.create(model=model_mapping[model], 
                                            messages=[{"role": "user", "content": msg},])
        res_msg = res.choices[0].message.content
    except Exception as e:
        print(f"Error: {e}")
        return None

    if print_on_screen:
        print(res_msg)
    else:
        return res_msg

def evaluate(code, model='p'):
    msg = f"评估以下代码:\n\n{code}\n\n"
    return ask(msg, model=model, print_on_screen=True)

def modify(code, model='p'):
    msg = f"优化以下代码:\n\n{code}\n\n"
    return ask(msg, model=model, print_on_screen=True)

@register_cell_magic
def e(line, cell):
    """
    Cell magic to evaluate Python code using the DeepSeek.deep_seeker.evaluate function.
    This function assumes the use of the 'p' model, which is tailored for code evaluation.
    """
    result = evaluate(cell, model='p')  # Assuming 'p' model is for code evaluation
    print(result)

@register_cell_magic
def m(line, cell):
    """
    Cell magic to modify Python code using the DeepSeek.deep_seeker.modify function.
    This function assumes the use of the 'p' model, which is tailored for code optimization.
    """
    result = modify(cell, model='p')
    print(result)
