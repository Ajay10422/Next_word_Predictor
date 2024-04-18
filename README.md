# NextWordPrediction

Flask app using 2 transformer models Bart and GPT2 to predict next word

Command to run: python -m flask —app .\app.py run

Required installations: Flask, Python, Torch, Transformers

Module 1 - Next Word Predictor 

Model 1 - BART - Fine-tuned with dataset containing transcripts of Ted talks.

Output 1 - Top 4 best suitable words for the given sentence.

Module 2 - Sentence Prediction.

Model 2 - GPT2 - Fine-tuned with the containing transcripts of Ted talks.

Output 2 - Gives top 4 meaningful sentences.
