import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

export default defineConfig({
  plugins: [react()],
  build: {
    outDir: 'dist',
    rollupOptions: {
      input: './src/main.jsx'
    }
  },
  server: {
    port: 3000
  },
  base: "/" // Netlify에서 루트 경로를 명확하게 지정
})
