# predictor/views.py
from django.shortcuts import render
import torch
from .models import InputText
from transformers import GPT2LMHeadModel, GPT2Tokenizer

# Load pre-trained model and tokenizer
model_name = "gpt2-medium"  # You can use other pre-trained models like "gpt2-large" or "gpt2-xl" for better performance
tokenizer = GPT2Tokenizer.from_pretrained(model_name)
model = GPT2LMHeadModel.from_pretrained(model_name)




def input_text(request):
    if request.method == 'POST':
        text = request.POST.get('text', '')
        InputText.objects.create(text=text)
    
        inputtext=text
            
        num_predictions=5
        input_ids = tokenizer.encode(inputtext, return_tensors="pt")

        # Generate predictions
        with torch.no_grad():
            outputs = model.generate(
                input_ids,
                max_length=len(input_ids[0]) + 20,  # Adjust maximum length as needed
                num_return_sequences=num_predictions,
                temperature=0.7,  # Adjust temperature for more diverse predictions
                pad_token_id=tokenizer.eos_token_id,  # End of text token
                bos_token_id=tokenizer.bos_token_id,  # Beginning of text token
                eos_token_id=tokenizer.eos_token_id,  # End of sequence token
                no_repeat_ngram_size=2,  # Prevent repetition of n-grams
                num_beams=5,  # Number of beams for beam search
                early_stopping=True  # Stop generation when all beams reach EOS token
            )

        predictions = []
        for output in outputs:
            predicted_text = tokenizer.decode(output, skip_special_tokens=True)
            predictions.append(predicted_text)
            result=predicted_text
    

        return render(request, 'output.html', {'prediction': result})
    return render(request, 'input.html') 