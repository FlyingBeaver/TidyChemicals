import { defineConfig } from 'vite'
import { resolve } from 'path'
import vue from '@vitejs/plugin-vue'

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [vue()],
  build: {
    rollupOptions: {
      input: {
        'create': resolve(__dirname, 'src/views/create/index.html'),
        'update-read': resolve(__dirname, 'src/views/update-read/index.html')
      }
    }
  },
})
