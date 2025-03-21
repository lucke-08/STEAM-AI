import bodyParser from 'body-parser';
import express from 'express';
import cors from 'cors';
import dotenv from 'dotenv';
import { Configuration, OpenAIApi } from 'openai';
import fs from 'fs';

dotenv.config();

const app = express();
const port = 8155;

const openai = new OpenAIApi(
  new Configuration({
    apiKey: process.env.OPENAI_API_KEY,
  })
);

// Middlewares
app.use(cors()); // Aggiungi il middleware CORS
app.use(bodyParser.json());

// Funzione per leggere il testo da un file .txt
async function getSystemPromptFromTxt() {
  try {
    const txtData = fs.readFileSync('prompt.txt', 'utf-8');
    return txtData.trim();
  } catch (error) {
    console.error('Errore nella lettura del file .txt:', error);
    throw error;
  }
}

// Endpoint per inviare messaggi al bot
app.post('/send_message_to_bot', async (req, res) => {
  const messages = req.body.messages;
  if (!messages || messages.length === 0) {
    return res.status(400).json({ error: 'Invalid request' });
  }

  const systemPrompt = await getSystemPromptFromTxt();

  try {
    const response = await openai.createChatCompletion({
      model: 'gpt-3.5-turbo',
      messages: [
        { 'role': 'system', 'content': systemPrompt }, // Usa il prompt di sistema estratto dal file .txt
        { 'role': 'user', 'content': messages[messages.length - 1].content }
      ],
    });

    const botResponse = response.data.choices[0].message.content;

    return res.status(200).json({ response: botResponse });
  } catch (error) {
    console.error('Error:', error);
    return res.status(500).json({ error: 'Internal server error' });
  }
});

// Avvio del server
app.listen(port, () => {
  console.log(`Server running at http://localhost:${port}`);
});