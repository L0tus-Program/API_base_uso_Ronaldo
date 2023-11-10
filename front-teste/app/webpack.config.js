const path = require('path');

module.exports = {
  // ... outras configurações do webpack ...

  resolve: {
    fallback: {
      "crypto": require.resolve("crypto-browserify"),
      "stream": require.resolve("stream-browserify"),
    }
  }
};
