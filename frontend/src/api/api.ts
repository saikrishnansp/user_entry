import axios from "axios"

// Create an Axios instance with base URL from .env
export const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL, // Reads from frontend .env
  withCredentials: false,
  headers: {
    "Content-Type": "application/json"
  }
})

