// This file will contain the functions for making API calls to the backend.

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

export async function runAgent(query) {
  const response = await fetch(`${API_URL}/agent`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ query }),
  });
  if (!response.ok) {
    const errorData = await response.text();
    throw new Error(`Backend Error: ${errorData}`);
  }
  return response.json();
}
