import React from "react";
import SongPlayer from "@/components/SongPlayer";

function SongList({ songs }) {
  return (
    <div className="mt-4">
      {songs.map((song, index) => (
        <div key={index} className="mb-4">
          <p className="font-bold">{song.name}</p>
          <p className="text-sm">{song.artist}</p>
          <SongPlayer url={song.url} previewUrl={song.preview_url} />
        </div>
      ))}
    </div>
  );
}

export default SongList;
