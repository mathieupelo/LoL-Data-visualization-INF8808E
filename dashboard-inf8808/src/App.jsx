import { useState } from 'react'
import Sidebar from './components/Sidebar'
import RadarChart from './components/RadarChart'
import ChartSection from './components/ChartSection'

export default function App() {
  const [selected, setSelected] = useState('Radar')

  return (
    <div className="flex h-screen bg-gray-100">
      <Sidebar selected={selected} setSelected={setSelected} />
      <div className="flex-1 flex flex-col">
        <header className="bg-white shadow px-6 py-6 text-center">
          <h2 className="text-3xl font-bold text-gray-800">Team 21</h2>
          <p className="mt-2 text-gray-500 text-lg">
            Welcome to our interactive dashboard
          </p>
        </header>
        <main className="flex-1 p-6">
        <ChartSection
          title="Titre de chart"
          description="Description du chart"
        >
        <RadarChart />  
        </ChartSection>

        </main>
      </div>
    </div>
  )
}
