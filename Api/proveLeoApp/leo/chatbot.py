from flask import Flask, request, jsonify
import nltk
from nltk.chat.util import Chat, reflections

# nltk.download('punkt') da runnare solo una volta per il download
# nltk.download('averaged_perceptron_tagger') da runnare solo una volta per il download
# nltk.download('wordnet') da runnare solo una volta per il download


pairs = [
    ['Cosa avete di disponibile?', ['Abbiamo una vasta gamma di auto disponibili. Quali sono le tue preferenze?']],
    ['Quanto costa una 'auto'?', ['Il prezzo di una Toyota Corolla varia a seconda dell'anno' e del 'modello'.']],
    ['Quali colori sono disponibili per la ['auto']?', ['Attualmente abbiamo disponibili i colori bianco, nero e grigio per la Toyota Corolla.']],
    ['Grazie', ['Prego, fammi sapere se hai altre domande.']]
