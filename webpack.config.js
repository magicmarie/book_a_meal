const path = require("path");
const ExtractTextPlugin = require("extract-text-webpack-plugin");
module.exports = {
    mode: process.env.NODE_ENV,
    entry: {
        css: "./src/sass/app.scss",
        js: "./src/js/app.js"
    },
    output: {
        path: path.resolve(__dirname, "UI"),
        filename: "[name]/app.[name]"
    },
    module: {
        rules: [
            {
                test: path.resolve(__dirname, "src/sass/app.scss"),
                use: ExtractTextPlugin.extract({
                    fallback: "style-loader",
                    use: ["css-loader", "sass-loader"]
                })
            }
        ]
    },
    plugins: [new ExtractTextPlugin("css/app.css")]
};