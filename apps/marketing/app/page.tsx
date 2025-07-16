export default function HomePage() {
  return (
    <div className="min-h-screen bg-gray-50">
      <div className="container mx-auto px-4 py-8">
        <div className="text-center">
          <h1 className="text-4xl font-bold text-gray-900 mb-6">
            Greek ERP/CRM System
          </h1>
          <p className="text-xl text-gray-600 mb-8">
            Revolutionary business management that eliminates CRM/ERP silos
          </p>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mt-12">
            <div className="bg-white rounded-lg shadow-md p-6">
              <h3 className="text-lg font-semibold text-gray-900 mb-4">
                Unified CRM+ERP
              </h3>
              <p className="text-gray-600">
                360° business view without system switching
              </p>
            </div>

            <div className="bg-white rounded-lg shadow-md p-6">
              <h3 className="text-lg font-semibold text-gray-900 mb-4">
                Greek Compliance
              </h3>
              <p className="text-gray-600">
                AADE integration and Greek tax compliance
              </p>
            </div>

            <div className="bg-white rounded-lg shadow-md p-6">
              <h3 className="text-lg font-semibold text-gray-900 mb-4">
                Smart Automation
              </h3>
              <p className="text-gray-600">
                AI-powered business process automation
              </p>
            </div>
          </div>

          <div className="mt-12 space-x-4">
            <button className="bg-primary text-white px-6 py-3 rounded-lg hover:bg-primary/90">
              Get Started
            </button>
            <button className="border border-gray-300 text-gray-700 px-6 py-3 rounded-lg hover:bg-gray-50">
              View Pricing
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}
