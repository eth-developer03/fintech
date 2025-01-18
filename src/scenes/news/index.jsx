import React, { useState } from 'react';

const NewsBoard = () => {
  const [iframeError, setIframeError] = useState(false);
  const stockNewsUrl = 'https://web-news-iwhdvddvapstytxauebj4u.streamlit.app/?embed=true';

  const handleIframeError = () => {
    setIframeError(true);
  };

  const openInNewTab = () => {
    window.open(stockNewsUrl, '_blank', 'noopener,noreferrer');
  };

  return (
    <div className="p-4">
      {!iframeError ? (
        <div className="relative" style={{ height: '600px' }}>
          <iframe
            src={stockNewsUrl}
            onError={handleIframeError}
            style={{
              width: '100%',
              height: '100%',
              border: '1px solid #ddd',
              borderRadius: '8px'
            }}
            sandbox="allow-same-origin allow-scripts allow-forms allow-popups"
          />
        </div>
      ) : (
        <div className="text-center p-8 border rounded-lg">
          <p className="mb-4">Unable to embed Stock News directly.</p>
          <button
            onClick={openInNewTab}
            className="px-4 py-2 bg-blue-500 text-white rounded hover:bg-blue-600 transition-colors"
          >
            Open in New Tab
          </button>
        </div>
      )}
    </div>
  );
};

export default NewsBoard;
// 53cd7e60682a4701a02c04d72a5e9e55