import React from 'react';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { BrowserRouter } from 'react-router-dom';
import { ThemeProvider, createTheme } from '@mui/material/styles';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import LoginPage from '../../pages/LoginPage';
import { useAuthStore } from '../../store/authStore';

// Mock the auth store
jest.mock('../../store/authStore');
const mockUseAuthStore = useAuthStore as jest.MockedFunction<typeof useAuthStore>;

// Mock react-router-dom
const mockNavigate = jest.fn();
jest.mock('react-router-dom', () => ({
  ...jest.requireActual('react-router-dom'),
  useNavigate: () => mockNavigate,
}));

const theme = createTheme();
const queryClient = new QueryClient({
  defaultOptions: {
    queries: { retry: false },
    mutations: { retry: false },
  },
});

const renderLoginPage = (authState = {}) => {
  mockUseAuthStore.mockReturnValue({
    login: jest.fn(),
    isLoading: false,
    error: null,
    clearError: jest.fn(),
    ...authState,
  } as any);

  return render(
    <QueryClientProvider client={queryClient}>
      <BrowserRouter>
        <ThemeProvider theme={theme}>
          <LoginPage />
        </ThemeProvider>
      </BrowserRouter>
    </QueryClientProvider>
  );
};

describe('LoginPage Component', () => {
  const user = userEvent.setup();

  beforeEach(() => {
    jest.clearAllMocks();
  });

  it('renders login form elements', () => {
    renderLoginPage();
    
    expect(screen.getByText('Bem-vindo de volta!')).toBeInTheDocument();
    expect(screen.getByText('Faça login para acessar sua conta')).toBeInTheDocument();
    expect(screen.getByLabelText(/nome de usuário ou email/i)).toBeInTheDocument();
    expect(screen.getByLabelText(/senha/i)).toBeInTheDocument();
    expect(screen.getByRole('button', { name: /entrar/i })).toBeInTheDocument();
  });

  it('shows password visibility toggle', async () => {
    renderLoginPage();
    
    const passwordInput = screen.getByLabelText(/senha/i);
    const toggleButton = screen.getByRole('button', { name: /toggle password visibility/i });
    
    expect(passwordInput).toHaveAttribute('type', 'password');
    
    await user.click(toggleButton);
    expect(passwordInput).toHaveAttribute('type', 'text');
    
    await user.click(toggleButton);
    expect(passwordInput).toHaveAttribute('type', 'password');
  });

  it('displays validation errors for empty fields', async () => {
    renderLoginPage();
    
    const submitButton = screen.getByRole('button', { name: /entrar/i });
    await user.click(submitButton);
    
    await waitFor(() => {
      expect(screen.getByText('Nome de usuário é obrigatório')).toBeInTheDocument();
      expect(screen.getByText('Senha é obrigatória')).toBeInTheDocument();
    });
  });

  it('displays validation error for short password', async () => {
    renderLoginPage();
    
    const usernameInput = screen.getByLabelText(/nome de usuário ou email/i);
    const passwordInput = screen.getByLabelText(/senha/i);
    const submitButton = screen.getByRole('button', { name: /entrar/i });
    
    await user.type(usernameInput, 'testuser');
    await user.type(passwordInput, '123');
    await user.click(submitButton);
    
    await waitFor(() => {
      expect(screen.getByText('Senha deve ter pelo menos 6 caracteres')).toBeInTheDocument();
    });
  });

  it('calls login function with correct credentials', async () => {
    const mockLogin = jest.fn().mockResolvedValue(undefined);
    renderLoginPage({ login: mockLogin });
    
    const usernameInput = screen.getByLabelText(/nome de usuário ou email/i);
    const passwordInput = screen.getByLabelText(/senha/i);
    const submitButton = screen.getByRole('button', { name: /entrar/i });
    
    await user.type(usernameInput, 'testuser');
    await user.type(passwordInput, 'password123');
    await user.click(submitButton);
    
    await waitFor(() => {
      expect(mockLogin).toHaveBeenCalledWith('testuser', 'password123');
    });
  });

  it('navigates to dashboard on successful login', async () => {
    const mockLogin = jest.fn().mockResolvedValue(undefined);
    renderLoginPage({ login: mockLogin });
    
    const usernameInput = screen.getByLabelText(/nome de usuário ou email/i);
    const passwordInput = screen.getByLabelText(/senha/i);
    const submitButton = screen.getByRole('button', { name: /entrar/i });
    
    await user.type(usernameInput, 'testuser');
    await user.type(passwordInput, 'password123');
    await user.click(submitButton);
    
    await waitFor(() => {
      expect(mockNavigate).toHaveBeenCalledWith('/dashboard');
    });
  });

  it('displays error message when login fails', () => {
    const errorMessage = 'Credenciais inválidas';
    renderLoginPage({ error: errorMessage });
    
    expect(screen.getByText(errorMessage)).toBeInTheDocument();
  });

  it('clears error when error alert is closed', async () => {
    const mockClearError = jest.fn();
    renderLoginPage({ 
      error: 'Some error',
      clearError: mockClearError 
    });
    
    const closeButton = screen.getByRole('button', { name: /close/i });
    await user.click(closeButton);
    
    expect(mockClearError).toHaveBeenCalled();
  });

  it('shows loading state during login', () => {
    renderLoginPage({ isLoading: true });
    
    const submitButton = screen.getByRole('button', { name: /entrando.../i });
    expect(submitButton).toBeDisabled();
  });

  it('has links to register and forgot password', () => {
    renderLoginPage();
    
    expect(screen.getByText('Registre-se aqui')).toBeInTheDocument();
    expect(screen.getByText('Esqueceu sua senha?')).toBeInTheDocument();
  });

  it('shows social login buttons', () => {
    renderLoginPage();
    
    expect(screen.getByRole('button', { name: /google/i })).toBeInTheDocument();
    expect(screen.getByRole('button', { name: /github/i })).toBeInTheDocument();
  });

  it('handles form submission with Enter key', async () => {
    const mockLogin = jest.fn().mockResolvedValue(undefined);
    renderLoginPage({ login: mockLogin });
    
    const usernameInput = screen.getByLabelText(/nome de usuário ou email/i);
    const passwordInput = screen.getByLabelText(/senha/i);
    
    await user.type(usernameInput, 'testuser');
    await user.type(passwordInput, 'password123');
    await user.keyboard('{Enter}');
    
    await waitFor(() => {
      expect(mockLogin).toHaveBeenCalledWith('testuser', 'password123');
    });
  });

  it('prevents multiple submissions while loading', async () => {
    const mockLogin = jest.fn().mockImplementation(() => new Promise(resolve => setTimeout(resolve, 1000)));
    renderLoginPage({ login: mockLogin, isLoading: true });
    
    const submitButton = screen.getByRole('button', { name: /entrando.../i });
    
    expect(submitButton).toBeDisabled();
    
    // Try to click multiple times
    await user.click(submitButton);
    await user.click(submitButton);
    
    // Should only be called once (if at all, since button is disabled)
    expect(mockLogin).toHaveBeenCalledTimes(0);
  });

  it('clears error when user starts typing', async () => {
    const mockClearError = jest.fn();
    renderLoginPage({ 
      error: 'Some error',
      clearError: mockClearError 
    });
    
    const usernameInput = screen.getByLabelText(/nome de usuário ou email/i);
    await user.type(usernameInput, 'a');
    
    // Error should be cleared when user starts typing
    expect(mockClearError).toHaveBeenCalled();
  });
});