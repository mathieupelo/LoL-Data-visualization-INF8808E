import React from "react";
import { useEffect, useState } from "react";
import Plot from "react-plotly.js";

const players = ["Faker", "Caps"];

export default function App() {
  const [data, setData] = useState({});
  const [selected, setSelected] = useState("Faker");

  useEffect(() => {
    fetch(`http://localhost:5000/api/wins-by-player?player=${selected}`)
      .then((res) => res.json())
      .then(setData);
  }, [selected]);

  return (
    <div style={{ padding: "2rem" }}>
      <h1>Performances de {selected}</h1>

      <select value={selected} onChange={(e) => setSelected(e.target.value)}>
        {players.map((p) => (
          <option key={p} value={p}>
            {p}
          </option>
        ))}
      </select>

      <Plot
        data={[
          {
            type: "bar",
            x: Object.keys(data),
            y: Object.values(data),
            marker: { color: "mediumvioletred" },
          },
        ]}
        layout={{
          title: `Victoires par champion pour ${selected}`,
          autosize: true,
        }}
      />
    </div>
  );
}
