import ollama
import json
import re

def get_healed_locator(html_source, failed_by, failed_value):
    # DOM cleanup to focus on structure and save LLM tokens
    clean_html = re.sub(r'<script.*?>.*?</script>', '', html_source, flags=re.DOTALL)
    clean_html = re.sub(r'<style.*?>.*?</style>', '', clean_html, flags=re.DOTALL)

    prompt = f"""
    You are an expert SDET. Your task is to heal a broken Selenium locator using ONLY the provided HTML.

    CONTEXT:
    The test failed to find this element: {failed_by}='{failed_value}'

    INSTRUCTIONS:
    1. ANALYZE: Look at the provided HTML below.
    2. MATCH: Find the element that performs the same function as the failed one.
    3. TAG RULE: If it's a login/submit action, look for <button> or <input type="submit">.
    4. NO BIAS: Do NOT use values from the examples below. Use ONLY values present in the "Current HTML" section.

    EXAMPLES (For format only):
    Example A:
    Old: id='old_id'
    HTML: <input name='new_name_attr' type='text'>
    Output: {{"by": "name", "value": "new_name_attr"}}

    Example B:
    Old: id='old_btn'
    HTML: <button class='new-btn-class'>Click Me</button>
    Output: {{"by": "class name", "value": "new-btn-class"}}

    CURRENT HTML TO ANALYZE:
    ```html
    {clean_html}
    ```
    
    Output (JSON only):
    """
    
    print("[LLM-ENGINE] Querying local Llama 3.2 to heal the broken locator...")
    
    try:
        response = ollama.chat(model='llama3.2', messages=[
            {'role': 'user', 'content': prompt}
        ])
        
        raw_reply = response['message']['content']
        json_match = re.search(r'\{[^{}]*\}', raw_reply)
        
        if json_match:
            return json.loads(json_match.group(0))
        else:
            raise ValueError("The model did not return a valid JSON.")
            
    except Exception as e:
        print(f"[LLM-ENGINE] Inference Error: {e}")
        return None