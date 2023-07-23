const { defineConfig } = require('@vue/cli-service')
module.exports = {
    transpileDependencies: true,
    publicPath: process.env.NODE_ENV === 'production' ? '/static/base_app/dist/' : 'http://127.0.0.1:8080',
    outputDir: '../../../../simple_base_project/base_app/static/base_app/dist',
    indexPath: '../../../templates/base-vue.html', // relative to outputDir!

    chainWebpack: config => {
        /*
        The arrow function in writeToDisk(...) tells the dev server to write
        only index.html to the disk.

        The indexPath option (see above) instructs Webpack to also rename
        index.html to base-vue.html and save it to Django templates folder.

        We don't need other assets on the disk (CSS, JS...) - the dev server
        can serve them from memory.

        See also:
        https://cli.vuejs.org/config/#indexpath
        https://webpack.js.org/configuration/dev-server/#devserverwritetodisk-
        */
        config.devServer
            .public('http://127.0.0.1:8080')
            .hotOnly(true)
            .headers({"Access-Control-Allow-Origin": "*"})
            .writeToDisk(true);
    }
}
