import React, { useState } from "react";
import MoodInput from "../components/MoodInput";
import SongList from "../components/SongList";
import { analyzeMood } from '@/api/api';

function Dashboard() {
  const [songs, setSongs] = useState([]);
  const [sentiment, setSentiment] = useState("");

  const handleMoodSubmit = async (text) => {
    const data = await analyzeMood(text);
    if (data) {
      setSentiment(data.sentiment);
      setSongs(data.songs);
    }
  };

  return (
    <div className="p-4 max-w-xl mx-auto">
      <h1 className="text-2xl font-bold mb-4">MoodTunes</h1>
      <MoodInput onSubmit={handleMoodSubmit} />
      {sentiment && <p className="mt-2">Detected Mood: {sentiment}</p>}
      <SongList songs={songs} />
    </div>
  );
}

export default Dashboard;
