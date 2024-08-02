const { defineConfig } = require("@vue/cli-service");
const webpack = require("webpack");

module.exports = defineConfig({
  transpileDependencies: true,
  devServer: {
    port: 8000,
    proxy: {
      "/api": {
        target: "http://0.0.0.0:8001",
        changeOrigin: true,
        // pathRewrite: { '^/api': '' },
      },
    },
  },
  configureWebpack: {
    // Define feature flags for better tree-shaking in production
    plugins: [
      new webpack.DefinePlugin({
        __VUE_OPTIONS_API__: JSON.stringify(true),
        __VUE_PROD_DEVTOOLS__: JSON.stringify(false),
        __VUE_PROD_HYDRATION_MISMATCH_DETAILS__: JSON.stringify(false),
      }),
    ],
  },
});
