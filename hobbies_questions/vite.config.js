import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// Elastic Beanstalk backend URL
const API_BASE_URL = 'http://hobbies-backend-env.eba-ecbytrzk.ap-southeast-2.elasticbeanstalk.com';

export default defineConfig({
  plugins: [react()],
  build: {
    outDir: 'dist'
  },
  define: {
    'import.meta.env.VITE_API_BASE_URL': JSON.stringify(API_BASE_URL)
  }
});
