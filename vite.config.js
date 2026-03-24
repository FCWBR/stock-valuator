import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// https://vite.dev/config/
export default defineConfig({
  plugins: [react()],
  // For GitHub Pages: replace 'stock-valuator' with your repo name
  base: '/stock-valuator/',
})
