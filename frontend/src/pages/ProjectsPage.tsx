import React, { useState, useCallback } from 'react';
import {
  Box,
  Container,
  Typography,
  Button,
  Grid,
  Card,
  CardContent,
  CardActions,
  Paper,
  Chip,
  IconButton,
  Menu,
  MenuItem,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  TextField,
  Alert,
  LinearProgress,
} from '@mui/material';
import {
  Add,
  MoreVert,
  PictureAsPdf,
  CloudUpload,
  Delete,
  Edit,
  Download,
  Visibility,
  DragIndicator,
} from '@mui/icons-material';
import { motion, AnimatePresence } from 'framer-motion';
import { useDropzone } from 'react-dropzone';
import { useNavigate } from 'react-router-dom';

interface PDFFile {
  id: string;
  name: string;
  size: number;
  preview?: string;
  pages?: number;
}

interface Project {
  id: string;
  name: string;
  description?: string;
  files: PDFFile[];
  createdAt: Date;
  status: 'draft' | 'processing' | 'completed';
}

const ProjectsPage: React.FC = () => {
  const navigate = useNavigate();
  const [projects, setProjects] = useState<Project[]>([
    {
      id: '1',
      name: 'Relatórios Mensais',
      description: 'Compilação de relatórios do mês',
      files: [
        { id: '1', name: 'relatorio-janeiro.pdf', size: 2048000, pages: 15 },
        { id: '2', name: 'relatorio-fevereiro.pdf', size: 1856000, pages: 12 },
      ],
      createdAt: new Date('2024-01-15'),
      status: 'completed',
    },
    {
      id: '2',
      name: 'Documentos Fiscais',
      description: 'Organização de documentos fiscais',
      files: [
        { id: '3', name: 'nota-fiscal-001.pdf', size: 512000, pages: 3 },
        { id: '4', name: 'nota-fiscal-002.pdf', size: 768000, pages: 5 },
        { id: '5', name: 'nota-fiscal-003.pdf', size: 1024000, pages: 7 },
      ],
      createdAt: new Date('2024-01-10'),
      status: 'processing',
    },
  ]);
  
  const [selectedFiles, setSelectedFiles] = useState<File[]>([]);
  const [newProjectDialog, setNewProjectDialog] = useState(false);
  const [newProjectName, setNewProjectName] = useState('');
  const [newProjectDescription, setNewProjectDescription] = useState('');
  const [anchorEl, setAnchorEl] = useState<null | HTMLElement>(null);
  const [selectedProject, setSelectedProject] = useState<string | null>(null);
  const [uploadProgress, setUploadProgress] = useState(0);
  const [isUploading, setIsUploading] = useState(false);

  const onDrop = useCallback((acceptedFiles: File[]) => {
    const pdfFiles = acceptedFiles.filter(file => file.type === 'application/pdf');
    setSelectedFiles(prev => [...prev, ...pdfFiles]);
  }, []);

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    accept: {
      'application/pdf': ['.pdf'],
    },
    multiple: true,
  });

  const handleCreateProject = () => {
    if (!newProjectName.trim()) return;
    
    const newProject: Project = {
      id: Date.now().toString(),
      name: newProjectName,
      description: newProjectDescription,
      files: [],
      createdAt: new Date(),
      status: 'draft',
    };
    
    setProjects(prev => [newProject, ...prev]);
    setNewProjectName('');
    setNewProjectDescription('');
    setNewProjectDialog(false);
  };

  const handleMenuClick = (event: React.MouseEvent<HTMLElement>, projectId: string) => {
    setAnchorEl(event.currentTarget);
    setSelectedProject(projectId);
  };

  const handleMenuClose = () => {
    setAnchorEl(null);
    setSelectedProject(null);
  };

  const handleDeleteProject = () => {
    if (selectedProject) {
      setProjects(prev => prev.filter(p => p.id !== selectedProject));
    }
    handleMenuClose();
  };

  const formatFileSize = (bytes: number) => {
    if (bytes === 0) return '0 Bytes';
    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
  };

  const getStatusColor = (status: Project['status']) => {
    switch (status) {
      case 'completed': return 'success';
      case 'processing': return 'warning';
      case 'draft': return 'default';
      default: return 'default';
    }
  };

  const getStatusText = (status: Project['status']) => {
    switch (status) {
      case 'completed': return 'Concluído';
      case 'processing': return 'Processando';
      case 'draft': return 'Rascunho';
      default: return 'Desconhecido';
    }
  };

  return (
    <Container maxWidth="xl">
      <Box sx={{ py: 4 }}>
        {/* Header */}
        <Box
          component={motion.div}
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6 }}
          sx={{ mb: 4, display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}
        >
          <Box>
            <Typography
              variant="h3"
              sx={
                fontWeight: 700,
                mb: 1,
                color: 'white',
              }
            >
              Meus Projetos
            </Typography>
            <Typography
              variant="h6"
              sx={
                color: 'rgba(255, 255, 255, 0.8)',
              }
            >
              Gerencie e organize seus projetos PDF
            </Typography>
          </Box>
          <Button
            variant="contained"
            startIcon={<Add />}
            onClick={() => setNewProjectDialog(true)}
            sx={
              px: 3,
              py: 1.5,
              fontSize: '1rem',
              fontWeight: 600,
              background: 'rgba(255, 255, 255, 0.2)',
              backdropFilter: 'blur(20px)',
              border: '1px solid rgba(255, 255, 255, 0.3)',
              color: 'white',
              '&:hover': {
                background: 'rgba(255, 255, 255, 0.3)',
              },
            }
          >
            Novo Projeto
          </Button>
        </Box>

        {/* Upload Area */}
        <Paper
          component={motion.div}
          initial={{ opacity: 0, y: 30 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6, delay: 0.1 }}
          sx={
            mb: 4,
            background: 'rgba(255, 255, 255, 0.95)',
            backdropFilter: 'blur(20px)',
            border: '1px solid rgba(255, 255, 255, 0.2)',
          }
        >
          <Box
            {...getRootProps()}
            sx={
              p: 4,
              textAlign: 'center',
              cursor: 'pointer',
              borderRadius: 2,
              border: isDragActive ? '2px dashed #2196F3' : '2px dashed #e0e0e0',
              backgroundColor: isDragActive ? 'rgba(33, 150, 243, 0.04)' : 'transparent',
              transition: 'all 0.3s ease',
              '&:hover': {
                borderColor: '#2196F3',
                backgroundColor: 'rgba(33, 150, 243, 0.04)',
              },
            }
          >
            <input {...getInputProps()} />
            <CloudUpload sx={{ fontSize: 48, color: 'primary.main', mb: 2 }} />
            <Typography variant="h6" sx={{ mb: 1, fontWeight: 600 }}>
              {isDragActive ? 'Solte os arquivos aqui' : 'Arraste arquivos PDF ou clique para selecionar'}
            </Typography>
            <Typography variant="body2" color="text.secondary">
              Suporte para múltiplos arquivos PDF • Máximo 50MB por arquivo
            </Typography>
            
            {selectedFiles.length > 0 && (
              <Box sx={{ mt: 3 }}>
                <Typography variant="subtitle2" sx={{ mb: 2 }}>
                  Arquivos selecionados ({selectedFiles.length}):
                </Typography>
                <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 1, justifyContent: 'center' }}>
                  {selectedFiles.map((file, index) => (
                    <Chip
                      key={index}
                      label={`${file.name} (${formatFileSize(file.size)})`}
                      onDelete={() => setSelectedFiles(prev => prev.filter((_, i) => i !== index))}
                      color="primary"
                      variant="outlined"
                    />
                  ))}
                </Box>
              </Box>
            )}
            
            {isUploading && (
              <Box sx={{ mt: 3 }}>
                <LinearProgress variant="determinate" value={uploadProgress} sx={{ mb: 1 }} />
                <Typography variant="caption" color="text.secondary">
                  Enviando arquivos... {uploadProgress}%
                </Typography>
              </Box>
            )}
          </Box>
        </Paper>

        {/* Projects Grid */}
        <Grid container spacing={3}>
          <AnimatePresence>
            {projects.map((project, index) => (
              <Grid item xs={12} md={6} lg={4} key={project.id}>
                <Card
                  component={motion.div}
                  initial={{ opacity: 0, y: 30 }}
                  animate={{ opacity: 1, y: 0 }}
                  exit={{ opacity: 0, y: -30 }}
                  transition={{ duration: 0.6, delay: index * 0.1 }}
                  whileHover={{ y: -8, transition: { duration: 0.3 } }}
                  sx={
                    height: '100%',
                    display: 'flex',
                    flexDirection: 'column',
                    background: 'rgba(255, 255, 255, 0.95)',
                    backdropFilter: 'blur(20px)',
                    border: '1px solid rgba(255, 255, 255, 0.2)',
                    '&:hover': {
                      boxShadow: '0 12px 40px rgba(0,0,0,0.15)',
                    },
                    transition: 'all 0.3s ease',
                  }
                >
                  <CardContent sx={{ flexGrow: 1, p: 3 }}>
                    <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', mb: 2 }}>
                      <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                        <PictureAsPdf sx={{ color: 'primary.main' }} />
                        <Chip
                          label={getStatusText(project.status)}
                          size="small"
                          color={getStatusColor(project.status)}
                        />
                      </Box>
                      <IconButton
                        size="small"
                        onClick={(e) => handleMenuClick(e, project.id)}
                      >
                        <MoreVert />
                      </IconButton>
                    </Box>
                    
                    <Typography variant="h6" sx={{ mb: 1, fontWeight: 600 }}>
                      {project.name}
                    </Typography>
                    
                    {project.description && (
                      <Typography variant="body2" color="text.secondary" sx={{ mb: 2 }}>
                        {project.description}
                      </Typography>
                    )}
                    
                    <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 2 }}>
                      <Typography variant="body2" color="text.secondary">
                        {project.files.length} arquivo{project.files.length !== 1 ? 's' : ''}
                      </Typography>
                      <Typography variant="caption" color="text.secondary">
                        {project.createdAt.toLocaleDateString('pt-BR')}
                      </Typography>
                    </Box>
                    
                    {project.status === 'processing' && (
                      <LinearProgress sx={{ borderRadius: 1 }} />
                    )}
                  </CardContent>
                  
                  <CardActions sx={{ p: 2, pt: 0 }}>
                    <Button
                      size="small"
                      startIcon={<Visibility />}
                      onClick={() => navigate(`/projects/${project.id}`)}
                    >
                      Visualizar
                    </Button>
                    {project.status === 'completed' && (
                      <Button
                        size="small"
                        startIcon={<Download />}
                        color="primary"
                      >
                        Download
                      </Button>
                    )}
                  </CardActions>
                </Card>
              </Grid>
            ))}
          </AnimatePresence>
        </Grid>

        {projects.length === 0 && (
          <Paper
            component={motion.div}
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ duration: 0.6 }}
            sx={
              p: 6,
              textAlign: 'center',
              background: 'rgba(255, 255, 255, 0.95)',
              backdropFilter: 'blur(20px)',
              border: '1px solid rgba(255, 255, 255, 0.2)',
            }
          >
            <PictureAsPdf sx={{ fontSize: 80, color: 'text.secondary', mb: 2 }} />
            <Typography variant="h5" sx={{ mb: 2, fontWeight: 600 }}>
              Nenhum projeto encontrado
            </Typography>
            <Typography variant="body1" color="text.secondary" sx={{ mb: 3 }}>
              Crie seu primeiro projeto para começar a organizar seus PDFs
            </Typography>
            <Button
              variant="contained"
              startIcon={<Add />}
              onClick={() => setNewProjectDialog(true)}
              sx={
                px: 4,
                py: 1.5,
                fontSize: '1rem',
                fontWeight: 600,
              }
            >
              Criar Primeiro Projeto
            </Button>
          </Paper>
        )}
      </Box>

      {/* Project Menu */}
      <Menu
        anchorEl={anchorEl}
        open={Boolean(anchorEl)}
        onClose={handleMenuClose}
        PaperProps={
          sx: {
            borderRadius: 2,
            boxShadow: '0 8px 32px rgba(0,0,0,0.1)',
          },
        }
      >
        <MenuItem onClick={handleMenuClose}>
          <Edit sx={{ mr: 1 }} />
          Editar
        </MenuItem>
        <MenuItem onClick={handleMenuClose}>
          <Download sx={{ mr: 1 }} />
          Download
        </MenuItem>
        <MenuItem onClick={handleDeleteProject} sx={{ color: 'error.main' }}>
          <Delete sx={{ mr: 1 }} />
          Excluir
        </MenuItem>
      </Menu>

      {/* New Project Dialog */}
      <Dialog
        open={newProjectDialog}
        onClose={() => setNewProjectDialog(false)}
        maxWidth="sm"
        fullWidth
        PaperProps={
          sx: {
            borderRadius: 3,
            background: 'rgba(255, 255, 255, 0.95)',
            backdropFilter: 'blur(20px)',
          },
        }
      >
        <DialogTitle sx={{ pb: 1 }}>
          <Typography variant="h5" sx={{ fontWeight: 600 }}>
            Criar Novo Projeto
          </Typography>
        </DialogTitle>
        <DialogContent>
          <TextField
            autoFocus
            margin="dense"
            label="Nome do projeto"
            fullWidth
            variant="outlined"
            value={newProjectName}
            onChange={(e) => setNewProjectName(e.target.value)}
            sx={{ mb: 2 }}
          />
          <TextField
            margin="dense"
            label="Descrição (opcional)"
            fullWidth
            multiline
            rows={3}
            variant="outlined"
            value={newProjectDescription}
            onChange={(e) => setNewProjectDescription(e.target.value)}
          />
        </DialogContent>
        <DialogActions sx={{ p: 3, pt: 1 }}>
          <Button onClick={() => setNewProjectDialog(false)}>
            Cancelar
          </Button>
          <Button
            onClick={handleCreateProject}
            variant="contained"
            disabled={!newProjectName.trim()}
            sx={
              px: 3,
              fontWeight: 600,
            }
          >
            Criar Projeto
          </Button>
        </DialogActions>
      </Dialog>
    </Container>
  );
};

export default ProjectsPage;