import React from 'react';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import { BrowserRouter } from 'react-router-dom';
import { ThemeProvider, createTheme } from '@mui/material/styles';
import Navbar from '../../components/Navbar';
import { useAuthStore } from '../../store/authStore';

// Mock the auth store
jest.mock('../../store/authStore');
const mockUseAuthStore = useAuthStore as jest.MockedFunction<typeof useAuthStore>;

// Mock react-router-dom
const mockNavigate = jest.fn();
jest.mock('react-router-dom', () => ({
  ...jest.requireActual('react-router-dom'),
  useNavigate: () => mockNavigate,
  useLocation: () => ({ pathname: '/' }),
}));

const theme = createTheme();

const renderNavbar = (authState = {}) => {
  mockUseAuthStore.mockReturnValue({
    user: null,
    isAuthenticated: false,
    logout: jest.fn(),
    ...authState,
  } as any);

  return render(
    <BrowserRouter>
      <ThemeProvider theme={theme}>
        <Navbar />
      </ThemeProvider>
    </BrowserRouter>
  );
};

describe('Navbar Component', () => {
  beforeEach(() => {
    jest.clearAllMocks();
  });

  it('renders logo and navigation items', () => {
    renderNavbar();
    
    expect(screen.getByText('📄 PDF Organizer')).toBeInTheDocument();
    expect(screen.getByText('Início')).toBeInTheDocument();
  });

  it('shows login and register buttons when not authenticated', () => {
    renderNavbar({ isAuthenticated: false });
    
    expect(screen.getByText('Entrar')).toBeInTheDocument();
    expect(screen.getByText('Registrar')).toBeInTheDocument();
  });

  it('shows user menu when authenticated', () => {
    const mockUser = {
      id: 1,
      username: 'testuser',
      email: 'test@example.com',
      full_name: 'Test User',
    };

    renderNavbar({
      isAuthenticated: true,
      user: mockUser,
    });
    
    expect(screen.getByText('Dashboard')).toBeInTheDocument();
    expect(screen.getByText('Projetos')).toBeInTheDocument();
    
    // User avatar should be present
    const avatar = screen.getByText('T'); // First letter of username
    expect(avatar).toBeInTheDocument();
  });

  it('navigates to login when login button is clicked', () => {
    renderNavbar({ isAuthenticated: false });
    
    const loginButton = screen.getByText('Entrar');
    fireEvent.click(loginButton);
    
    expect(mockNavigate).toHaveBeenCalledWith('/login');
  });

  it('navigates to register when register button is clicked', () => {
    renderNavbar({ isAuthenticated: false });
    
    const registerButton = screen.getByText('Registrar');
    fireEvent.click(registerButton);
    
    expect(mockNavigate).toHaveBeenCalledWith('/register');
  });

  it('opens user menu when avatar is clicked', async () => {
    const mockUser = {
      id: 1,
      username: 'testuser',
      email: 'test@example.com',
      full_name: 'Test User',
    };

    renderNavbar({
      isAuthenticated: true,
      user: mockUser,
    });
    
    const avatar = screen.getByText('T');
    fireEvent.click(avatar);
    
    await waitFor(() => {
      expect(screen.getByText('Perfil')).toBeInTheDocument();
      expect(screen.getByText('Configurações')).toBeInTheDocument();
      expect(screen.getByText('Sair')).toBeInTheDocument();
    });
  });

  it('calls logout when logout menu item is clicked', async () => {
    const mockLogout = jest.fn();
    const mockUser = {
      id: 1,
      username: 'testuser',
      email: 'test@example.com',
      full_name: 'Test User',
    };

    renderNavbar({
      isAuthenticated: true,
      user: mockUser,
      logout: mockLogout,
    });
    
    // Open user menu
    const avatar = screen.getByText('T');
    fireEvent.click(avatar);
    
    // Click logout
    await waitFor(() => {
      const logoutButton = screen.getByText('Sair');
      fireEvent.click(logoutButton);
    });
    
    expect(mockLogout).toHaveBeenCalled();
    expect(mockNavigate).toHaveBeenCalledWith('/');
  });

  it('navigates to home when logo is clicked', () => {
    renderNavbar();
    
    const logo = screen.getByText('📄 PDF Organizer');
    fireEvent.click(logo);
    
    expect(mockNavigate).toHaveBeenCalledWith('/');
  });

  it('shows mobile menu button on small screens', () => {
    // Mock useMediaQuery to return true for mobile
    jest.mock('@mui/material/useMediaQuery', () => jest.fn(() => true));
    
    renderNavbar();
    
    // Mobile menu button should be present
    const menuButton = screen.getByLabelText('open drawer');
    expect(menuButton).toBeInTheDocument();
  });

  it('highlights current page in navigation', () => {
    // Mock useLocation to return dashboard path
    jest.doMock('react-router-dom', () => ({
      ...jest.requireActual('react-router-dom'),
      useLocation: () => ({ pathname: '/dashboard' }),
    }));

    renderNavbar({
      isAuthenticated: true,
      user: { username: 'testuser' },
    });
    
    const dashboardLink = screen.getByText('Dashboard');
    expect(dashboardLink).toHaveStyle({ color: 'primary.main' });
  });

  it('renders correctly with different user data', () => {
    const mockUser = {
      id: 1,
      username: 'johndoe',
      email: 'john@example.com',
      full_name: 'John Doe',
      avatar_url: 'https://example.com/avatar.jpg',
    };

    renderNavbar({
      isAuthenticated: true,
      user: mockUser,
    });
    
    // Should show first letter of username if no avatar
    const avatar = screen.getByText('J');
    expect(avatar).toBeInTheDocument();
  });

  it('handles navigation menu items correctly', () => {
    renderNavbar({
      isAuthenticated: true,
      user: { username: 'testuser' },
    });
    
    const dashboardLink = screen.getByText('Dashboard');
    fireEvent.click(dashboardLink);
    
    expect(mockNavigate).toHaveBeenCalledWith('/dashboard');
    
    const projectsLink = screen.getByText('Projetos');
    fireEvent.click(projectsLink);
    
    expect(mockNavigate).toHaveBeenCalledWith('/projects');
  });
});