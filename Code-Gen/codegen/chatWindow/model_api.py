from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from transformers import pipeline, AutoTokenizer, AutoModelForCausalLM
from fastapi.responses import JSONResponse

# Initialize FastAPI
app = FastAPI()

# Load the model
tokenizer = AutoTokenizer.from_pretrained("Salesforce/codegen-2B-mono")
model = AutoModelForCausalLM.from_pretrained("Salesforce/codegen-2B-mono")
pipe = pipeline("text-generation", model=model, tokenizer=tokenizer)

# Request and response models
class PromptRequest(BaseModel):
    prompt: str

@app.post("/generate-code")
async def generate_code(request: PromptRequest):
    prompt = request.prompt

    try:
        # Generate code from the prompt using the loaded model
        generated_code = pipe(prompt, max_length=500, do_sample=True, top_k=50, truncation=True)[0]['generated_text']
        
        return JSONResponse(content={'generated_code': generated_code})

    except Exception as e:
        # Log the error to the console
        print(f"Error: {e}")
        raise HTTPException(status_code=500, detail=str(e))
