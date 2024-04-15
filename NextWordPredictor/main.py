# %%
import torch
import string

from transformers import GPT2LMHeadModel, GPT2Tokenizer
from transformers import BartTokenizer, BartForConditionalGeneration
bart_model = BartForConditionalGeneration.from_pretrained(r"C:\Users\ajayk\OneDrive\Desktop\backup\Capstone1.pkl").eval()
bart_tokenizer = BartTokenizer.from_pretrained(r"C:\Users\ajayk\OneDrive\Desktop\Tokens")

GPT_model = GPT2LMHeadModel.from_pretrained(r"C:\Users\ajayk\OneDrive\Desktop\Capstone.pkl")
GPT_tokenizer = GPT2Tokenizer.from_pretrained(r"C:\Users\ajayk\OneDrive\Desktop\TokensGPT")

from happytransformer import TTSettings
from autocorrect import Speller
from happytransformer import HappyTextToText

top_k = 10

def decode(tokenizer, pred_idx, top_clean):
    ignore_tokens = string.punctuation + '[PAD]'
    tokens = []
    for w in pred_idx:
        token = ''.join(tokenizer.decode(w).split())
        if token not in ignore_tokens:
            tokens.append(token.replace('##', ''))
    return '\n'.join(tokens[:top_clean])


def encode(tokenizer, text_sentence, add_special_tokens=True):
    text_sentence = text_sentence.replace('<mask>', tokenizer.mask_token)
    # if <mask> is the last token, append a "." so that models dont predict punctuation.
    if tokenizer.mask_token == text_sentence.split()[-1]:
        text_sentence += ' .'

    input_ids = torch.tensor([tokenizer.encode(text_sentence, add_special_tokens=add_special_tokens)])
    mask_idx = torch.where(input_ids == tokenizer.mask_token_id)[1].tolist()[0]
    return input_ids, mask_idx


def get_all_predictions(text_sentence, top_clean=5):
    
    # ========================= BART =================================
    input_ids, mask_idx = encode(bart_tokenizer, text_sentence, add_special_tokens=True)
    with torch.no_grad():
        predict = bart_model(input_ids)[0]
    bart = decode(bart_tokenizer, predict[0, mask_idx, :].topk(top_k).indices.tolist(), top_clean)

    return {
            'bart': bart,
            }

def get_sentence_predictions(text_sentence):
    
   

    ##########################Correction###############################

    happy_tt = HappyTextToText("T5", "t5-base")


    happy_tt.model = happy_tt.model.from_pretrained(r"C:\Users\ajayk\OneDrive\Desktop\Grammarcorrection")

    text_sentence="grammar: "+text_sentence
    
    beam_settings =  TTSettings(num_beams=5, min_length=1, max_length=len(text_sentence))

    result_1 = happy_tt.generate_text(text_sentence, args=beam_settings)

    spell = Speller(lang='en')

    # Correct the spellings
    text_sentence = spell(result_1.text)

    Corrected_sentence="T5 Grammar and Spelling Corrected: "+text_sentence

    #######################Grammar Correction########################
    input_ids = GPT_tokenizer.encode(text_sentence, return_tensors="pt")

    num_outputs = 4  # Number of outputs to generate
    generated_texts = []

    for _ in range(num_outputs):

        # Generate text using the fine-tuned GPT-2 model
        output = GPT_model.generate(input_ids, 
                                max_length=100, 
                                num_return_sequences=1,
                                do_sample=True,  # Enable sampling
                                top_k=50,  
                                pad_token_id=GPT_tokenizer.eos_token_id)

        # Decode generated text
        generated_text = GPT_tokenizer.decode(output[0], skip_special_tokens=True)

        # Find the position of the first period
        period_position = generated_text.find(".")

        # Print the substring up to the first period
        if period_position != -1:
            generated_text = generated_text[:period_position + 1]  # Include the period
            
        generated_texts.append(generated_text)

    filtered_Text="\n".join(generated_texts)
    filtered_Text="GPT2 Generated Texts"+"\n"+filtered_Text
    Final_result=Corrected_sentence+"\n"+filtered_Text

    return {
            'bart': Final_result
    }