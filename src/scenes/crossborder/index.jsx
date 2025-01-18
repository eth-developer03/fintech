import React, { useState, useEffect } from 'react';

const CrossBorder = () => {
  const [dashboardError, setDashboardError] = useState(false);
  const dashboardUrl = 'https://itemcrossbordercomplience.streamlit.app/?embed=true';

  const handleDashboardError = () => {
    setDashboardError(true);
  };

  const openDashboardInNewTab = () => {
    window.open(dashboardUrl, '_blank', 'noopener,noreferrer');
  };

  return (
    <div className="p-4">
      {!dashboardError ? (
        <div className="relative" style={{ height: '600px' }}>
          <iframe
            src={dashboardUrl}
            onError={handleDashboardError}
            style={{
              width: '100%',
              height: '100%',
              border: '1px solid #ddd',
              borderRadius: '8px'
            }}
            sandbox="allow-same-origin allow-scripts allow-forms allow-popups"
            // referrerPolicy="strict-origin-when-cross-origin"
          />
        </div>
      ) : (
        <div className="text-center p-8 border rounded-lg">
          <p className="mb-4">Unable to embed the GDP Dashboard directly.</p>
          <button
            onClick={openDashboardInNewTab}
            className="px-4 py-2 bg-blue-500 text-white rounded hover:bg-blue-600 transition-colors"
          >
            Open in New Tab
          </button>
        </div>
      )}
    </div>
  );
};

export default CrossBorder;
