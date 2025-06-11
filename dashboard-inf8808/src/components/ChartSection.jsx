export default function ChartSection({ title, description, children }) {
    return (
      <div className="flex gap-6 p-6">
        <div className="w-1/2">
          <h3 className="text-xl font-semibold text-gray-800 mb-2">{title}</h3>
          <p className="text-gray-600 leading-relaxed">{description}</p>
        </div>
  
        <div className="w-1/2 border border-dashed border-gray-400 rounded-lg p-4 flex items-center justify-center bg-white">
          {children}
        </div>
      </div>
    )
  }
  