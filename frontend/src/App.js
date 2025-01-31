import { useState } from "react";
import axios from "axios";

function App() {
  const [feedback, setFeedback] = useState("");
  const [response, setResponse] = useState({
    sentiment: "",
    response_text: "",
    audio_url: "http://example.com/audio.mp3"
  });
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

  const handlePlay = async () => {
    if (response.response_text) {
      try {
        const result = await axios.post("http://localhost:8000/submit-feedback/", {
          feedback: response.response_text,
        });

        setResponse(prev => ({ ...prev, audio_url: result.data.audio_url }));
        setError(null);
      } catch (error) {
        setError(error.response ? error.response.data : "Something went wrong!");
      }
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

      <p><strong>Sentiment:</strong> {response.sentiment}</p>

      {response && (
        <div style={{ marginTop: "60px", textAlign: "center" }}>
          <h3>Generated Response</h3>
          <div style={{
            border: "1px solid #ccc",
            padding: "10px",
            borderRadius: "4px",
            backgroundColor: "#f9f9f9",
            minHeight: "100px"
          }}>
            <p>{response.response_text}</p>
          </div>
          <div style={{ display: "flex", justifyContent: "center", marginTop: "10px" }}>
            <button
              style={{ padding: "8px 16px", cursor: "pointer", marginRight: "10px" }}
              onClick={handlePlay}
            >
              Play
            </button>
            <button
              style={{ padding: "8px 16px", cursor: "pointer" }}
              onClick={() => alert('Download button clicked')}
            >
              Download
            </button>
          </div>
        </div>
      )}

      {error && <p style={{ color: "red", marginTop: "20px" }}>{error}</p>}
    </div>
  );
}

export default App;