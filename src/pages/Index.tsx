
import React, { useState, useEffect } from 'react';
import DesignerDirectory from "@/components/DesignerDirectory";

const Index = () => {
  const [apiTest, setApiTest] = useState<string>('Testing...');
  const [showMain, setShowMain] = useState(false);

  useEffect(() => {
    // Quick API test with environment variable
    const apiUrl = import.meta.env.VITE_API_BASE_URL || 'http://localhost:5001/api';

    fetch(`${apiUrl}/health`)
      .then(res => {
        if (!res.ok) {
          throw new Error(`HTTP ${res.status}: ${res.statusText}`);
        }
        return res.json();
      })
      .then(data => {
        setApiTest('API Connected ✅');
        setTimeout(() => setShowMain(true), 1000);
      })
      .catch(err => {
        setApiTest(`API Error: ${err.message} ❌`);
        setTimeout(() => setShowMain(true), 2000);
      });
  }, []);

  if (!showMain) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center">
          <div className="w-8 h-8 mx-auto mb-4">
            <img src="/lovable-uploads/de251bab-7a07-4dd1-ab51-268854eca36e.png" alt="EmptyCup" />
          </div>
          <h1 className="text-xl font-semibold mb-2">EmptyCup</h1>
          <p className="text-gray-600">{apiTest}</p>
          <p className="text-xs text-gray-400 mt-2">
            API URL: {import.meta.env.VITE_API_BASE_URL || 'http://localhost:5001/api'}
          </p>
        </div>
      </div>
    );
  }

  return <DesignerDirectory />;
};

export default Index;
