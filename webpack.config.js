const autoprefixer = require('autoprefixer');
const path = require('path');

module.exports = {
    mode: 'production',
    entry: [
        './static/css/app.scss',
        './static/js/app.js',
    ],
    output: {
        path: path.resolve('./static/js'),
        filename: 'bundle.js',
    },
    module: {
        rules: [
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
            {
                test: /\.js$/,
                loader: 'babel-loader',
                query: {
                    presets: [
                        '@babel/preset-env',
                    ],
                },
            },
        ],
    },
};
