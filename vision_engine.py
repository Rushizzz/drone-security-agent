import torch
from transformers import AutoProcessor, AutoModelForCausalLM
from PIL import Image

# 1. Hardware setup: Using CUDA for your RTX 3060 Ti 
device = "cuda" if torch.cuda.is_available() else "cpu"
model_id = "multimodalart/Florence-2-large-no-flash-attn"

# 2. Model initialization
# We use attn_implementation="sdpa" to avoid the flash_attn requirement in WSL.
print(f"Loading {model_id} on {device}...")
model = AutoModelForCausalLM.from_pretrained(
    model_id, 
    trust_remote_code=True, 
    attn_implementation="sdpa"
).to(device).eval()

processor = AutoProcessor.from_pretrained(model_id, trust_remote_code=True)

def get_vlm_description(image_path, task_prompt="<DETAILED_CAPTION>"):
    """
    Analyzes an image and returns a detailed text description[cite: 80].
    """
    try:
        # Load and prepare the image
        image = Image.open(image_path).convert("RGB")
        
        # Preprocess inputs
        inputs = processor(text=task_prompt, images=image, return_tensors="pt").to(device)
        
        # Generate the visual analysis [cite: 13]
        generated_ids = model.generate(
            input_ids=inputs["input_ids"],
            pixel_values=inputs["pixel_values"],
            max_new_tokens=1024,
            num_beams=3,
            do_sample=False
        )
        
        # Decode the raw model output into text [cite: 80]
        generated_text = processor.batch_decode(generated_ids, skip_special_tokens=False)[0]
        
        # Post-process for the specific task format
        parsed_answer = processor.post_process_generation(
            generated_text, 
            task=task_prompt, 
            image_size=(image.width, image.height)
        )
        
        return parsed_answer[task_prompt]
    
    except Exception as e:
        return f"Error processing frame: {str(e)}"