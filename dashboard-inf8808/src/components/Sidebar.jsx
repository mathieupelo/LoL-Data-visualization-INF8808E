const charts = ['Radar', 'Line', 'Scatter', 'Bar', 'Pie', 'autre a definir']

export default function Sidebar({ selected, setSelected }) {
  return (
    <aside className="w-60 bg-gray-900 text-white p-4 space-y-4">
      <h1 className="text-2xl font-bold mb-6">Dashboard</h1>
      {charts.map((chart) => (
        <button
          key={chart}
          onClick={() => setSelected(chart)}
          className={`w-full text-left px-3 py-2 rounded ${
            selected === chart ? 'bg-gray-700' : 'hover:bg-gray-800'
          }`}
        >
          {chart} Chart
        </button>
      ))}
    </aside>
  )
}
