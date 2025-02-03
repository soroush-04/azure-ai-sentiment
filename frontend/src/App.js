import { useState, useEffect } from "react";
import axios from "axios";
import './App.css';
import config from './config';

function App() {
  const [feedback, setFeedback] = useState("");
  const [response, setResponse] = useState({
    sentiment: "",
    response_text: "",
    audio_url: "http://example.com/audio.mp3"
  });
  const [error, setError] = useState(null);
  const [loading, setLoading] = useState(false);
  const [loadingDots, setLoadingDots] = useState(".");

  useEffect(() => {
    let interval;
    if (loading) {
      interval = setInterval(() => {
        setLoadingDots((prev) => {
          if (prev === "...") return ".";
          return prev + ".";
        });
      }, 500); // Change dots every 500ms
    } else {
      setLoadingDots(".");
    }

    return () => clearInterval(interval);
  }, [loading]);

  const API_URL = config.API_URL; // Switch API_URL from the config file

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      setLoading(true);
      const result = await axios.post(`${API_URL}/submit-feedback/`, {
        feedback: feedback,
      });

      setResponse(result.data);
      setError(null);
    } catch (error) {
      setError(error.response ? error.response.data : "Something went wrong!");
      setResponse(null);
    } finally {
      setLoading(false);
    }
  };

  const handlePlay = async () => {
    if (response.response_text && response.sentiment) {
      try {
        const result = await axios.post(`${API_URL}/play-response/`, {
          feedback: response.response_text,
          sentiment: response.sentiment,
        });

        console.log("Audio file URL:", result.data.audio_url);
        const audioUrl = `${API_URL}${result.data.audio_url}`;

        const audio = new Audio(audioUrl);
        audio.play();

        setResponse((prev) => ({ ...prev, audio_url: result.data.audio_url }));
        setError(null);
      } catch (error) {
        setError(error.response ? error.response.data : "Something went wrong!");
      } finally {
      }
    }
  };

  const handleDownload = () => {
    const audioUrl = `${API_URL}/download-audio/`;
    const link = document.createElement("a");
    link.href = audioUrl;
    link.setAttribute("download", "output.mp3");
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);

    alert("Download started!");
  };

  return (
    <div className="container">
      <h2>Submit Your Feedback</h2>
      <form onSubmit={handleSubmit} className="form-container">
        <textarea
          value={feedback}
          onChange={(e) => setFeedback(e.target.value)}
          placeholder="Share your feedback with us ..."
          className="textarea"
        />
        <div className="button-container">
        <button type="submit" disabled={!feedback.trim()}>Submit</button>
        </div>
      </form>

      <p className="sentiment">
        <strong>Sentiment:</strong> {""}
        {loading ? <span className="loading-animation">{loadingDots}</span> : response.sentiment}
      </p>

      <div className="response-box">
        <h3>Generated Response</h3>
        <div className="response-text">
          {loading ? (
            <p className="loading-animation">{loadingDots}</p>
          ) : response.response_text}
        </div>
        <div className="button-container">
          <button disabled={!response.response_text} className="play-button" onClick={handlePlay}>
            Play
          </button>
          <button disabled={!response.response_text} className="download-button" onClick={handleDownload}>
            Download
          </button>
        </div>
      </div>
      {error && <p className="error-message">{error}</p>}
    </div>
  );
}

export default App;