import { useState } from "react";

function App() {
  const [feedback, setFeedback] = useState("");

  const handleSubmit = (e) => {
    e.preventDefault();
    console.log("Feedback submitted:", feedback);
    setFeedback(""); //clear
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
        <button type="submit" style={{ marginTop: "10px", padding: "8px 16px" }}>
          Submit
        </button>
      </form>
    </div>
  );
}

export default App;
