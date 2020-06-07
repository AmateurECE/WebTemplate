const path = require('path');
module.exports = {
    mode: "production",
    entry: './source/js/main.js',
    output: {
        path: path.resolve('./source/build'),
        filename: 'bundle.js'
    },
    module: {
        rules: [
            { test: /\.js$/, use: 'babel-loader' }
        ]
    },
    stats: {
        colors: true
    },
    devtool: 'source-map',
    externals: {
        'd3': 'd3'
    }
};
