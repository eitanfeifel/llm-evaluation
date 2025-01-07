import express from "express";
import bodyParser from "body-parser";
import axios from "axios";

const app = express();
const PORT = 3000;

// Middleware
app.use(bodyParser.json());
app.use(express.static("public"));


// Endpoint to handle user input and call backend
app.post("/prompt", async (req, res) => {
  //console.log("body:", req.body)
  const {task, prompt } = req.body;
  try {
    const backendResponse = await axios.post("http://localhost:8000/generate/", {
        task,
        prompt,
    });
    const { responses, evaluations, results } = backendResponse.data;
    res.json({ responses, evaluations, results });
  } catch (error) {
    res.status(500).json({ error: "Failed to get response from backend." });
  }
});

// Start the server
app.listen(PORT, () => {
  console.log(`Frontend server running at http://localhost:${PORT}`);
});
