
const path = require('path');
const UglifyJsWebpackPlugin = require('uglifyjs-webpack-plugin');

module.exports = {
  plugins: [
    new UglifyJsWebpackPlugin()
  ],
  entry: {
    'main': './src/App.js'
  },
  output: {
    filename: 'js/[name].js',
    path: path.resolve(__dirname, 'static')
  },
  module: {
    loaders: [
      {
        test: /\.js/,
        include: [path.resolve(__dirname, 'src')],
        loader: 'babel-loader'
      }
    ]
  }
};
