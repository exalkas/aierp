export default function HomePage() {
  return (
    <div className="container mx-auto px-4 py-8">
      <div className="text-center">
        <h1 className="text-4xl font-bold text-maritime-blue mb-6">
          Axiologic
        </h1>
        <p className="text-xl text-gray-600 mb-8">
          Comprehensive business management for Greek companies
        </p>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 mt-12">
          <div className="bg-white rounded-lg shadow-md p-6 hover:shadow-lg transition-shadow">
            <h3 className="text-lg font-semibold text-gray-900 mb-4">
              CRM Module
            </h3>
            <p className="text-gray-600">
              Manage customers, leads, and sales opportunities
            </p>
          </div>
          <div className="bg-white rounded-lg shadow-md p-6 hover:shadow-lg transition-shadow">
            <h3 className="text-lg font-semibold text-gray-900 mb-4">
              ERP Module
            </h3>
            <p className="text-gray-600">
              Invoicing, inventory, and financial management
            </p>
          </div>
          <div className="bg-white rounded-lg shadow-md p-6 hover:shadow-lg transition-shadow">
            <h3 className="text-lg font-semibold text-gray-900 mb-4">
              Greek Compliance
            </h3>
            <p className="text-gray-600">
              AADE integration and Greek tax compliance
            </p>
          </div>
        </div>
      </div>
    </div>
  );
}
