const { defineConfig } = require('@vue/cli-service')
module.exports = defineConfig({
  transpileDependencies: true,
  outputDir: '../../../../simple_base_project/base_app/static/base_app',
  indexPath: '../../../../simple_base_project/base_app/templates',
  assetsDir: '',
  publicPath: 'static'
})
