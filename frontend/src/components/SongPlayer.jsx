import React from "react";

function SongPlayer({ url, previewUrl }) {
  return previewUrl ? (
    <audio controls src={previewUrl}></audio>
  ) : (
    <iframe
      src={`https://open.spotify.com/embed/track/${url.split("/track/")[1]}`}
      width="300"
      height="80"
      frameBorder="0"
      allowtransparency="true"
      allow="encrypted-media"
      title="Spotify Player"
    ></iframe>
  );
}

export default SongPlayer;
