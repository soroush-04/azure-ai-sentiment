import { useState } from "react";
import axios from "axios";

function App() {
  const [feedback, setFeedback] = useState("");
  const [response, setResponse] = useState(null);
  const [error, setError] = useState(null);

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    try {
      const result = await axios.post("http://localhost:8000/submit-feedback/", {
        feedback: feedback,
      });

      setResponse(result.data);
      setError(null);
      // setFeedback(""); //clear
    } catch (error) {
      setError(error.response ? error.response.data : "Something went wrong!");
      setResponse(null);
    }
  };

  return (
    <div style={{ maxWidth: "400px", margin: "50px auto", textAlign: "center" }}>
      <h2>Submit Your Feedback</h2>
      <form onSubmit={handleSubmit}>
        <textarea
          value={feedback}
          onChange={(e) => setFeedback(e.target.value)}
          placeholder="Share your feedback with us ..."
          rows="5"
          style={{ width: "100%", padding: "10px" }}
        />
        <br />
        <button
          type="submit"
          style={{ marginTop: "10px", padding: "8px 16px", cursor: "pointer" }}
        >
          Submit
        </button>
      </form>

      {response && (
        <div style={{ marginTop: "20px" }}>
          <h3>Sentiment: {response.sentiment}</h3>
          <p>Generated Response: {response.response_text}</p>
        </div>
      )}

      {error && <p style={{ color: "red", marginTop: "20px" }}>{error}</p>}
    </div>
  );
}

export default App;
