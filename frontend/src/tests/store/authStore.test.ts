import { renderHook, act } from '@testing-library/react';
import axios from 'axios';
import { useAuthStore } from '../../store/authStore';

// Mock axios
jest.mock('axios');
const mockedAxios = axios as jest.Mocked<typeof axios>;

// Mock localStorage
const localStorageMock = {
  getItem: jest.fn(),
  setItem: jest.fn(),
  removeItem: jest.fn(),
  clear: jest.fn(),
};
Object.defineProperty(window, 'localStorage', {
  value: localStorageMock,
});

describe('AuthStore', () => {
  beforeEach(() => {
    jest.clearAllMocks();
    // Reset store state
    useAuthStore.setState({
      user: null,
      token: null,
      isAuthenticated: false,
      isLoading: false,
      error: null,
    });
  });

  describe('login', () => {
    it('successfully logs in user', async () => {
      const mockResponse = {
        data: {
          access_token: 'mock-token',
          user: {
            id: 1,
            username: 'testuser',
            email: 'test@example.com',
            full_name: 'Test User',
          },
        },
      };

      mockedAxios.post.mockResolvedValueOnce(mockResponse);

      const { result } = renderHook(() => useAuthStore());

      await act(async () => {
        await result.current.login('testuser', 'password123');
      });

      expect(result.current.isAuthenticated).toBe(true);
      expect(result.current.user).toEqual(mockResponse.data.user);
      expect(result.current.token).toBe('mock-token');
      expect(result.current.error).toBeNull();
      expect(result.current.isLoading).toBe(false);
    });

    it('handles login failure', async () => {
      const mockError = {
        response: {
          data: {
            detail: 'Credenciais inválidas',
          },
        },
      };

      mockedAxios.post.mockRejectedValueOnce(mockError);

      const { result } = renderHook(() => useAuthStore());

      await act(async () => {
        try {
          await result.current.login('testuser', 'wrongpassword');
        } catch (error) {
          // Expected to throw
        }
      });

      expect(result.current.isAuthenticated).toBe(false);
      expect(result.current.user).toBeNull();
      expect(result.current.token).toBeNull();
      expect(result.current.error).toBe('Credenciais inválidas');
      expect(result.current.isLoading).toBe(false);
    });

    it('sets loading state during login', async () => {
      let resolvePromise: (value: any) => void;
      const mockPromise = new Promise((resolve) => {
        resolvePromise = resolve;
      });

      mockedAxios.post.mockReturnValueOnce(mockPromise);

      const { result } = renderHook(() => useAuthStore());

      act(() => {
        result.current.login('testuser', 'password123');
      });

      expect(result.current.isLoading).toBe(true);

      await act(async () => {
        resolvePromise!({
          data: {
            access_token: 'mock-token',
            user: { id: 1, username: 'testuser' },
          },
        });
        await mockPromise;
      });

      expect(result.current.isLoading).toBe(false);
    });

    it('sets axios authorization header on successful login', async () => {
      const mockResponse = {
        data: {
          access_token: 'mock-token',
          user: { id: 1, username: 'testuser' },
        },
      };

      mockedAxios.post.mockResolvedValueOnce(mockResponse);

      const { result } = renderHook(() => useAuthStore());

      await act(async () => {
        await result.current.login('testuser', 'password123');
      });

      expect(mockedAxios.defaults.headers.common['Authorization']).toBe(
        'Bearer mock-token'
      );
    });
  });

  describe('register', () => {
    it('successfully registers and logs in user', async () => {
      const registerResponse = {
        data: {
          id: 1,
          username: 'newuser',
          email: 'new@example.com',
        },
      };

      const loginResponse = {
        data: {
          access_token: 'mock-token',
          user: registerResponse.data,
        },
      };

      mockedAxios.post
        .mockResolvedValueOnce(registerResponse) // register call
        .mockResolvedValueOnce(loginResponse); // login call

      const { result } = renderHook(() => useAuthStore());

      const userData = {
        username: 'newuser',
        email: 'new@example.com',
        password: 'password123',
        full_name: 'New User',
      };

      await act(async () => {
        await result.current.register(userData);
      });

      expect(result.current.isAuthenticated).toBe(true);
      expect(result.current.user).toEqual(registerResponse.data);
    });

    it('handles registration failure', async () => {
      const mockError = {
        response: {
          data: {
            detail: 'Usuário já existe',
          },
        },
      };

      mockedAxios.post.mockRejectedValueOnce(mockError);

      const { result } = renderHook(() => useAuthStore());

      const userData = {
        username: 'existinguser',
        email: 'existing@example.com',
        password: 'password123',
      };

      await act(async () => {
        try {
          await result.current.register(userData);
        } catch (error) {
          // Expected to throw
        }
      });

      expect(result.current.error).toBe('Usuário já existe');
      expect(result.current.isAuthenticated).toBe(false);
    });
  });

  describe('logout', () => {
    it('clears user data and token', () => {
      const { result } = renderHook(() => useAuthStore());

      // Set initial authenticated state
      act(() => {
        useAuthStore.setState({
          user: { id: 1, username: 'testuser' },
          token: 'mock-token',
          isAuthenticated: true,
        });
      });

      act(() => {
        result.current.logout();
      });

      expect(result.current.user).toBeNull();
      expect(result.current.token).toBeNull();
      expect(result.current.isAuthenticated).toBe(false);
      expect(result.current.error).toBeNull();
    });

    it('removes axios authorization header', () => {
      const { result } = renderHook(() => useAuthStore());

      // Set initial token
      mockedAxios.defaults.headers.common['Authorization'] = 'Bearer mock-token';

      act(() => {
        result.current.logout();
      });

      expect(mockedAxios.defaults.headers.common['Authorization']).toBeUndefined();
    });
  });

  describe('clearError', () => {
    it('clears error state', () => {
      const { result } = renderHook(() => useAuthStore());

      // Set initial error
      act(() => {
        useAuthStore.setState({ error: 'Some error' });
      });

      expect(result.current.error).toBe('Some error');

      act(() => {
        result.current.clearError();
      });

      expect(result.current.error).toBeNull();
    });
  });

  describe('setLoading', () => {
    it('sets loading state', () => {
      const { result } = renderHook(() => useAuthStore());

      act(() => {
        result.current.setLoading(true);
      });

      expect(result.current.isLoading).toBe(true);

      act(() => {
        result.current.setLoading(false);
      });

      expect(result.current.isLoading).toBe(false);
    });
  });

  describe('refreshToken', () => {
    it('refreshes token successfully', async () => {
      const mockResponse = {
        data: {
          access_token: 'new-mock-token',
        },
      };

      mockedAxios.post.mockResolvedValueOnce(mockResponse);

      const { result } = renderHook(() => useAuthStore());

      // Set initial token
      act(() => {
        useAuthStore.setState({ token: 'old-token' });
      });

      await act(async () => {
        await result.current.refreshToken();
      });

      expect(result.current.token).toBe('new-mock-token');
      expect(mockedAxios.defaults.headers.common['Authorization']).toBe(
        'Bearer new-mock-token'
      );
    });

    it('logs out user when refresh fails', async () => {
      mockedAxios.post.mockRejectedValueOnce(new Error('Refresh failed'));

      const { result } = renderHook(() => useAuthStore());

      // Set initial authenticated state
      act(() => {
        useAuthStore.setState({
          user: { id: 1, username: 'testuser' },
          token: 'old-token',
          isAuthenticated: true,
        });
      });

      await act(async () => {
        await result.current.refreshToken();
      });

      expect(result.current.user).toBeNull();
      expect(result.current.token).toBeNull();
      expect(result.current.isAuthenticated).toBe(false);
    });

    it('does nothing when no token exists', async () => {
      const { result } = renderHook(() => useAuthStore());

      await act(async () => {
        await result.current.refreshToken();
      });

      expect(mockedAxios.post).not.toHaveBeenCalled();
    });
  });

  describe('persistence', () => {
    it('persists authentication state', () => {
      const { result } = renderHook(() => useAuthStore());

      act(() => {
        useAuthStore.setState({
          user: { id: 1, username: 'testuser' },
          token: 'mock-token',
          isAuthenticated: true,
        });
      });

      // Check if localStorage.setItem was called
      expect(localStorageMock.setItem).toHaveBeenCalled();
    });
  });
});