// This file will contain the functions for making API calls to the backend.
// For now, it's a placeholder.

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

export async function login(email, password) {
  const response = await fetch(`${API_URL}/token`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
    body: new URLSearchParams({ username: email, password: password }),
  });
  if (!response.ok) {
    throw new Error('Login failed');
  }
  return response.json();
}
