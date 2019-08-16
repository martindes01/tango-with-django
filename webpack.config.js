const autoprefixer = require('autoprefixer');
const path = require('path');

module.exports = {
  mode: 'production',
  entry: [
    './src/app.js',
    './src/app.scss',
  ],
  output: {
    path: path.resolve('./static/js'),
    filename: 'bundle.js',
  },
  module: {
    rules: [
      {
        test: /\.js$/,
        loader: 'babel-loader',
        query: {
          presets: [
            '@babel/preset-env',
          ],
        },
      },
      {
        test: /\.scss$/,
        use: [
          {
            loader: 'file-loader',
            options: {
              name: '../css/bundle.css',
            },
          },
          {
            loader: 'extract-loader',
          },
          {
            loader: 'css-loader',
          },
          {
            loader: 'postcss-loader',
            options: {
              plugins: () => [
                autoprefixer(),
              ],
            },
          },
          {
            loader: 'sass-loader',
            options: {
              includePaths: [
                './node_modules',
              ],
            },
          },
        ],
      },
    ],
  },
};
