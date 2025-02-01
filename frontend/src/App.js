import { useState } from "react";
import axios from "axios";
import './App.css';

function App() {
  const [feedback, setFeedback] = useState("");
  const [response, setResponse] = useState({
    sentiment: "",
    response_text: "",
    audio_url: "http://example.com/audio.mp3"
  });
  const [audio, setAudio] = useState(false);
  const [error, setError] = useState(null);

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    try {
      setAudio(true)
      const result = await axios.post("http://localhost:8000/submit-feedback/", {
        feedback: feedback,
      });

      setResponse(result.data);
      setError(null);
    } catch (error) {
      setError(error.response ? error.response.data : "Something went wrong!");
      setResponse(null);
    }
    finally {
      setAudio(false)
    }
  };

  const handlePlay = async () => {
    if (response.response_text) {
      try {
        setAudio(true)
        const result = await axios.post("http://localhost:8000/submit-feedback/", {
          feedback: response.response_text,
        });

        setResponse(prev => ({ ...prev, audio_url: result.data.audio_url }));
        setError(null);
      } catch (error) {
        setError(error.response ? error.response.data : "Something went wrong!");
      }
      finally {
        setAudio(false)
      }
    }
  };

  return (
    <div className="container">
      {/* <div className="header">
        Soroush Kami <br />
        Full Stack Developer for AI Solution
      </div> */}
      <h2>Submit Your Feedback</h2>
      <form onSubmit={handleSubmit} className="form-container">
        <textarea
          value={feedback}
          onChange={(e) => setFeedback(e.target.value)}
          placeholder="Share your feedback with us ..."
          className="textarea"
        />
        <div className="button-container">
        <button type="submit" disabled={audio}>Submit</button>
        </div>
      </form>

      <p className="sentiment"><strong>Sentiment:</strong> {response.sentiment}</p>

      {response && (
        <div className="response-box">
          <h3>Generated Response</h3>
          <div className="response-text">
            <p>{response.response_text}</p>
          </div>
          <div className="button-container">
            <button disabled={audio} className="play-button" onClick={handlePlay}>
              Play
            </button>
          </div>
        </div>
      )}

      {error && <p className="error-message">{error}</p>}
    </div>
  );
}

export default App;