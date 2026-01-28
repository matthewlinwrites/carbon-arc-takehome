import { apiClient } from './client'
import type { LoginRequest, LoginResponse } from '../types/auth'

export async function login(credentials: LoginRequest): Promise<LoginResponse> {
  const response = await apiClient.post<LoginResponse>('/auth/login', credentials)
  return response.data
}
