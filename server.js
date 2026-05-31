const express = require('express');
const { OpenAI } = require('openai');
const path = require('path');

const app = express();
const PORT = process.env.PORT || 3000;

// Initialize OpenAI client for Navy API
const client = new OpenAI({
  apiKey: process.env.NAVY_API_KEY || "sk-navy-CPFLtUUlVBr6LKSuK3LrUDYCVXdsua-OgMkdJ6wPcBY",
  baseURL: "https://api.navy/v1"
});

app.use(express.json());
app.use(express.static(path.join(__dirname, 'public')));

// API endpoint to generate explanation for incorrect answers
app.post('/api/explain', async (req, res) => {
  const { question, userAnswer, correctAnswer } = req.body;

  if (!question || !userAnswer || !correctAnswer) {
    return res.status(400).json({ error: "Missing required fields: question, userAnswer, correctAnswer" });
  }

  try {
    const prompt = `Tu es un instructeur CCNA expert. Un étudiant a donné une réponse incorrecte à la question suivante.
Question: ${question}
Sa réponse (incorrecte): ${userAnswer}
La réponse correcte: ${correctAnswer}

Explique-lui clairement et de manière encourageante pourquoi sa réponse est fausse, et détaille le fonctionnement ou le concept réseau derrière la bonne réponse. Reste concis (maximum 3-4 phrases) et réponds impérativement en français.`;

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
    console.error("Error communicating with Navy API:", error);
    res.status(500).json({ error: "Une erreur est survenue lors de la communication avec le service d'explications." });
  }
});

app.listen(PORT, () => {
  console.log(`Server is running on http://localhost:${PORT}`);
});
