import { setupServer } from 'msw/node';
import { rest } from 'msw';

const API_BASE_URL = 'http://localhost:8000/api';

// Mock data
const mockUser = {
  id: 1,
  username: 'testuser',
  email: 'test@example.com',
  full_name: 'Test User',
  is_active: true,
  is_superuser: false,
  created_at: '2024-01-01T00:00:00Z',
};

const mockProjects = [
  {
    id: 1,
    name: 'Test Project 1',
    description: 'A test project',
    owner_id: 1,
    is_public: false,
    status: 'completed',
    created_at: '2024-01-01T00:00:00Z',
    updated_at: '2024-01-01T00:00:00Z',
  },
  {
    id: 2,
    name: 'Test Project 2',
    description: 'Another test project',
    owner_id: 1,
    is_public: true,
    status: 'draft',
    created_at: '2024-01-02T00:00:00Z',
    updated_at: '2024-01-02T00:00:00Z',
  },
];

const mockFiles = [
  {
    id: 1,
    project_id: 1,
    original_filename: 'document1.pdf',
    stored_filename: 'uuid1.pdf',
    file_path: '/uploads/uuid1.pdf',
    file_size: 1024000,
    page_count: 5,
    order_index: 0,
    thumbnail_path: '/uploads/uuid1_thumb.png',
    created_at: '2024-01-01T00:00:00Z',
  },
  {
    id: 2,
    project_id: 1,
    original_filename: 'document2.pdf',
    stored_filename: 'uuid2.pdf',
    file_path: '/uploads/uuid2.pdf',
    file_size: 2048000,
    page_count: 10,
    order_index: 1,
    thumbnail_path: '/uploads/uuid2_thumb.png',
    created_at: '2024-01-01T00:00:00Z',
  },
];

// Request handlers
export const handlers = [
  // Authentication endpoints
  rest.post(`${API_BASE_URL}/auth/login`, (req, res, ctx) => {
    return res(
      ctx.status(200),
      ctx.json({
        access_token: 'mock-jwt-token',
        token_type: 'bearer',
        expires_in: 1800,
        user: mockUser,
      })
    );
  }),

  rest.post(`${API_BASE_URL}/auth/register`, (req, res, ctx) => {
    return res(
      ctx.status(200),
      ctx.json(mockUser)
    );
  }),

  rest.post(`${API_BASE_URL}/auth/refresh`, (req, res, ctx) => {
    return res(
      ctx.status(200),
      ctx.json({
        access_token: 'new-mock-jwt-token',
        token_type: 'bearer',
        expires_in: 1800,
      })
    );
  }),

  rest.post(`${API_BASE_URL}/auth/logout`, (req, res, ctx) => {
    return res(
      ctx.status(200),
      ctx.json({ message: 'Logout realizado com sucesso' })
    );
  }),

  // User endpoints
  rest.get(`${API_BASE_URL}/users/me`, (req, res, ctx) => {
    return res(
      ctx.status(200),
      ctx.json(mockUser)
    );
  }),

  rest.put(`${API_BASE_URL}/users/me`, (req, res, ctx) => {
    return res(
      ctx.status(200),
      ctx.json({ ...mockUser, ...req.body })
    );
  }),

  rest.get(`${API_BASE_URL}/users/stats`, (req, res, ctx) => {
    return res(
      ctx.status(200),
      ctx.json({
        total_projects: 5,
        total_operations: 15,
        operations_by_type: {
          merge: 8,
          compress: 4,
          split: 3,
        },
        member_since: '2024-01-01T00:00:00Z',
      })
    );
  }),

  // Project endpoints
  rest.get(`${API_BASE_URL}/pdf/projects/`, (req, res, ctx) => {
    return res(
      ctx.status(200),
      ctx.json(mockProjects)
    );
  }),

  rest.post(`${API_BASE_URL}/pdf/projects/`, (req, res, ctx) => {
    const newProject = {
      id: 3,
      ...req.body,
      owner_id: 1,
      status: 'draft',
      created_at: new Date().toISOString(),
      updated_at: new Date().toISOString(),
    };
    return res(
      ctx.status(200),
      ctx.json(newProject)
    );
  }),

  rest.get(`${API_BASE_URL}/pdf/projects/:id`, (req, res, ctx) => {
    const { id } = req.params;
    const project = mockProjects.find(p => p.id === parseInt(id as string));
    
    if (!project) {
      return res(
        ctx.status(404),
        ctx.json({ detail: 'Projeto não encontrado' })
      );
    }
    
    return res(
      ctx.status(200),
      ctx.json(project)
    );
  }),

  // File upload
  rest.post(`${API_BASE_URL}/pdf/projects/:id/upload`, (req, res, ctx) => {
    return res(
      ctx.status(200),
      ctx.json(mockFiles)
    );
  }),

  // File reorder
  rest.put(`${API_BASE_URL}/pdf/projects/:id/reorder`, (req, res, ctx) => {
    return res(
      ctx.status(200),
      ctx.json({ message: 'Ordem dos arquivos atualizada' })
    );
  }),

  // PDF merge
  rest.post(`${API_BASE_URL}/pdf/projects/:id/merge`, (req, res, ctx) => {
    return res(
      ctx.status(200),
      ctx.json({
        message: 'PDFs mesclados com sucesso',
        output_path: '/outputs/merged.pdf',
        total_pages: 15,
        operation_id: 1,
      })
    );
  }),

  // Download
  rest.get(`${API_BASE_URL}/pdf/projects/:id/download`, (req, res, ctx) => {
    return res(
      ctx.status(200),
      ctx.set('Content-Type', 'application/pdf'),
      ctx.set('Content-Disposition', 'attachment; filename="merged.pdf"'),
      ctx.body('mock-pdf-content')
    );
  }),

  // Operations
  rest.get(`${API_BASE_URL}/pdf/operations/`, (req, res, ctx) => {
    return res(
      ctx.status(200),
      ctx.json([
        {
          id: 1,
          user_id: 1,
          project_id: 1,
          operation_type: 'merge',
          status: 'completed',
          created_at: '2024-01-01T00:00:00Z',
          completed_at: '2024-01-01T00:01:00Z',
        },
      ])
    );
  }),

  // Health check
  rest.get(`${API_BASE_URL.replace('/api', '')}/health`, (req, res, ctx) => {
    return res(
      ctx.status(200),
      ctx.json({
        status: 'healthy',
        version: '3.0.0',
        timestamp: new Date().toISOString(),
      })
    );
  }),

  // Error handlers
  rest.get(`${API_BASE_URL}/error`, (req, res, ctx) => {
    return res(
      ctx.status(500),
      ctx.json({ detail: 'Internal server error' })
    );
  }),

  rest.get(`${API_BASE_URL}/unauthorized`, (req, res, ctx) => {
    return res(
      ctx.status(401),
      ctx.json({ detail: 'Could not validate credentials' })
    );
  }),
];

// Setup server
export const server = setupServer(...handlers);