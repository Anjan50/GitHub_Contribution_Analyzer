import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

export default defineConfig({
  plugins: [react()],
  server: {
    host: '0.0.0.0',  // Make the app accessible from any network interface
    port: 5173,        // You can specify the port here (5173 is default)
    proxy: {
      '/api': {
        target: 'http://152.7.178.147:5000',
        changeOrigin: true,
        secure: false,
      },
      '/oauth': {
        target: 'http://152.7.178.147:5000',
        changeOrigin: true,
        secure: false,
      }
    }
  }
})
