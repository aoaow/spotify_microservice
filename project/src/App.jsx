import React, { useState } from 'react';
import { useQuery } from '@tanstack/react-query';
import axios from 'axios';

function App() {
  const [selectedDate, setSelectedDate] = useState('');
  const [selectedRegion, setSelectedRegion] = useState('');
  const [selectedArtist, setSelectedArtist] = useState('');

  // Fetch filters (dates, regions, artists)
  const {
    data: filters,
    isLoading: loadingFilters,
    error: errorFilters
  } = useQuery(['filters'], () =>
    axios.get('/filters').then(res => res.data)
  );

  // Fetch tracks based on selected filters
  const {
    data: tracksData,
    isLoading: loadingTracks,
    error: errorTracks
  } = useQuery(['tracks', selectedDate, selectedRegion, selectedArtist], () =>
    axios.get('/tracks', {
      params: {
        date: selectedDate,
        region: selectedRegion,
        artist: selectedArtist
      }
    }).then(res => res.data)
  );

  // Handle loading and error states
  if (loadingFilters || loadingTracks) {
    return <div className="p-8">Loading...</div>;
  }

  if (errorFilters || errorTracks) {
    return <div className="p-8">Error loading data</div>;
  }

  // Safely use filters and tracks data
  const dates = filters?.dates || [];
  const regions = filters?.regions || [];
  const artists = filters?.artists || [];
  const tracks = tracksData || [];

  return (
    <div className="bg-gray-100 min-h-screen p-8">
      <div className="max-w-7xl mx-auto">
        <h1 className="text-3xl font-bold mb-8">Spotify Top Tracks Analytics</h1>

        {/* Dropdowns for filters */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-8">
          <select
            className="p-2 border rounded"
            value={selectedDate}
            onChange={(e) => setSelectedDate(e.target.value)}
          >
            <option value="">Select Date</option>
            {dates.map((date) => (
              <option key={date} value={date}>
                {date}
              </option>
            ))}
          </select>

          <select
            className="p-2 border rounded"
            value={selectedRegion}
            onChange={(e) => setSelectedRegion(e.target.value)}
          >
            <option value="">Select Region</option>
            {regions.map((region) => (
              <option key={region} value={region}>
                {region}
              </option>
            ))}
          </select>

          <select
            className="p-2 border rounded"
            value={selectedArtist}
            onChange={(e) => setSelectedArtist(e.target.value)}
          >
            <option value="">Select Artist</option>
            {artists.map((artist) => (
              <option key={artist} value={artist}>
                {artist}
              </option>
            ))}
          </select>
        </div>

        {/* Tracks Table */}
        <div className="bg-white rounded-lg shadow overflow-hidden">
          <table className="min-w-full">
            <thead>
              <tr className="bg-gray-50">
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Rank</th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Track</th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Artist</th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Streams</th>
              </tr>
            </thead>
            <tbody className="bg-white divide-y divide-gray-200">
              {tracks.map((track, index) => (
                <tr key={`${track.track_title}-${track.artist}-${index}`}>
                  <td className="px-6 py-4 whitespace-nowrap">{track.global_rank}</td>
                  <td className="px-6 py-4 whitespace-nowrap">
                    <a
                      href={track.track_url}
                      className="text-blue-600 hover:text-blue-900"
                      target="_blank"
                      rel="noopener noreferrer"
                    >
                      {track.track_title}
                    </a>
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap">{track.artist}</td>
                  <td className="px-6 py-4 whitespace-nowrap">{Number(track.track_streams).toLocaleString()}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
}

export default App;