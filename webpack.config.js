const path = require('path');

module.exports = {
  entry: './static/js/index.js',
  output: {
    filename: 'bundle.js',
    path: path.resolve(__dirname, './static/js/dist'),

  },
  module: {
    rules: [
      {
        test: /\.css$/,
        use: ['style-loader', 'css-loader'],
      },
      {
        test: /\.scss$/,
        use: ['style-loader', 'css-loader', 'sass-loader'],
      },
    ],
  },
  resolve: {
  modules: [path.resolve(__dirname, './node_modules')], // Include node_modules path
  // ...other options (if any)
},

};

console.log(path.resolve(__dirname, './static/js/dist'));


