const express = require('express');
const { OpenAI } = require('openai');
const path = require('path');

const app = express();
const PORT = process.env.PORT || 3000;

// Initialize OpenAI client for MNN AI API
const client = new OpenAI({
  apiKey: process.env.MNN_API_KEY || "mnn-key-lLZXqyzSOT9kmoAutI4r92UkDlpsmt",
  baseURL: "https://api.mnnai.ru/v1"
});

app.use(express.json());
app.use(express.static(path.join(__dirname, 'public')));

// API endpoint to generate explanation for incorrect answers
app.post('/api/explain', async (req, res) => {
  const { question, userAnswer, correctAnswer } = req.body;

  if (!question || !userAnswer || !correctAnswer) {
    return res.status(400).json({ error: "Missing required fields: question, userAnswer, correctAnswer" });
  }

  const prompt = `Tu es un instructeur CCNA expert. Un étudiant a donné une réponse incorrecte à la question suivante.
Question: ${question}
Sa réponse (incorrecte): ${userAnswer}
La réponse correcte: ${correctAnswer}

Explique-lui clairement et de manière encourageante pourquoi sa réponse est fausse, et détaille le fonctionnement ou le concept réseau derrière la bonne réponse. Reste concis (maximum 3-4 phrases) et réponds impérativement en français.`;

  try {
    const response = await client.chat.completions.create({
      model: "gpt-4o-mini",
      messages: [
        { role: "system", content: "Tu es un assistant pédagogique spécialisé dans les réseaux informatiques et les certifications Cisco CCNA." },
        { role: "user", content: prompt }
      ]
    });

    const explanation = response.choices[0].message.content;
    res.json({ explanation });

  } catch (error) {
    console.error("Error communicating with MNN AI API:", error.message);
    // Return 200 with null so the frontend hides the AI box gracefully
    res.status(200).json({ explanation: null, error: "Service IA temporairement indisponible." });
  }
});

app.listen(PORT, () => {
  console.log(`Server is running on http://localhost:${PORT}`);
});
