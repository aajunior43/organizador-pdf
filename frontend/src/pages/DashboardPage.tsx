import React from 'react';
import {
  Box,
  Container,
  Typography,
  Grid,
  Card,
  CardContent,
  Button,
  Paper,
  LinearProgress,
  Chip,
  Avatar,
  List,
  ListItem,
  ListItemText,
  ListItemIcon,
  Divider,
} from '@mui/material';
import {
  PictureAsPdf,
  Add,
  Folder,
  TrendingUp,
  Schedule,
  CheckCircle,
  CloudUpload,
  Compress,
  Security,
} from '@mui/icons-material';
import { motion } from 'framer-motion';
import { useNavigate } from 'react-router-dom';
import { useAuthStore } from '../store/authStore';

const DashboardPage: React.FC = () => {
  const navigate = useNavigate();
  const { user } = useAuthStore();

  const stats = [
    {
      title: 'Total de Projetos',
      value: '12',
      change: '+3 este mês',
      icon: <Folder sx={{{ fontSize: 40 }} />,
      color: '#2196F3',
    },
    {
      title: 'PDFs Processados',
      value: '248',
      change: '+45 esta semana',
      icon: <PictureAsPdf sx={{{ fontSize: 40 }} />,
      color: '#4CAF50',
    },
    {
      title: 'Espaço Economizado',
      value: '2.4 GB',
      change: 'Compressão média: 65%',
      icon: <Compress sx={{{ fontSize: 40 }} />,
      color: '#FF9800',
    },
    {
      title: 'Operações Seguras',
      value: '156',
      change: '100% protegidas',
      icon: <Security sx={{{ fontSize: 40 }} />,
      color: '#9C27B0',
    },
  ];

  const recentProjects = [
    {
      name: 'Relatórios Mensais',
      files: 8,
      status: 'Concluído',
      date: '2 horas atrás',
    },
    {
      name: 'Documentos Fiscais',
      files: 15,
      status: 'Em andamento',
      date: '1 dia atrás',
    },
    {
      name: 'Contratos 2024',
      files: 23,
      status: 'Concluído',
      date: '3 dias atrás',
    },
  ];

  const quickActions = [
    {
      title: 'Novo Projeto',
      description: 'Criar um novo projeto PDF',
      icon: <Add />,
      action: () => navigate('/projects/new'),
      color: '#2196F3',
    },
    {
      title: 'Upload Rápido',
      description: 'Fazer upload de arquivos',
      icon: <CloudUpload />,
      action: () => navigate('/upload'),
      color: '#4CAF50',
    },
    {
      title: 'Meus Projetos',
      description: 'Ver todos os projetos',
      icon: <Folder />,
      action: () => navigate('/projects'),
      color: '#FF9800',
    },
  ];

  return (
    <Container maxWidth="xl">
      <Box sx={{{ py: 4 }}>
        {/* Header */}}
        <Box
          component={motion.div}}
          initial={{ opacity: 0, y: 20 }}}
          animate={{ opacity: 1, y: 0 }}}
          transition={{ duration: 0.6 }}}
          sx={{{ mb: 4 }}}
        >
          <Typography
            variant="h3"
            sx={{
              fontSize: { xs: '2.5rem', md: '3.5rem', lg: '4rem' },
              fontWeight: 700,
              mb: 2,
              color: 'white',
            }}
          >
            Olá, {user?.full_name || user?.username}! 👋
          </Typography>
          <Typography
            variant="h6"
            sx={{
               color: 'rgba(255, 255, 255, 0.8)',
               mb: 3,
             }}
          >
            Bem-vindo ao seu dashboard. Aqui você pode gerenciar todos os seus projetos PDF.
          </Typography>
        </Box>

        {/* Stats Cards */}}
        <Grid container spacing={3} sx={{{ mb: 4 }}>
          {stats.map((stat, index) => (
            <Grid item xs={12} sm={6} lg={3} key={index}>
              <Card
                component={motion.div}}
                initial={{ opacity: 0, y: 30 }}}
                animate={{ opacity: 1, y: 0 }}}
                transition={{ duration: 0.6, delay: index * 0.1 }}}
                whileHover={{ y: -5, transition: { duration: 0.2 } }}}
                sx={{
                  height: '100%',
                  background: 'rgba(255, 255, 255, 0.95)',
                  backdropFilter: 'blur(20px)',
                  border: '1px solid rgba(255, 255, 255, 0.2)',
                }}
              >
                <CardContent sx={{{ p: 3 }}>
                  <Box sx={{{ display: 'flex', alignItems: 'center', mb: 2 }}>
                    <Box
                      sx={{
                        p: 1.5,
                        borderRadius: 2,
                        backgroundColor: `${stat.color}15`,
                        color: stat.color,
                        mr: 2,
                      }}
                    >
                      {stat.icon}}
                    </Box>
                    <Box>
                      <Typography variant="h4" sx={{{ fontWeight: 700, mb: 0.5 }}>
                        {stat.value}}
                      </Typography>
                      <Typography variant="body2" color="text.secondary">
                        {stat.title}}
                      </Typography>
                    </Box>
                  </Box>
                  <Typography variant="caption" color="text.secondary">
                    {stat.change}}
                  </Typography>
                </CardContent>
              </Card>
            </Grid>
          ))}}
        </Grid>

        <Grid container spacing={3}>
          {/* Quick Actions */}}
          <Grid item xs={12} md={4}>
            <Paper
              component={motion.div}}
              initial={{ opacity: 0, x: -30 }}}
              animate={{ opacity: 1, x: 0 }}}
              transition={{ duration: 0.6, delay: 0.2 }}}
              sx={{
                p: 3,
                height: 'fit-content',
                background: 'rgba(255, 255, 255, 0.95)',
                backdropFilter: 'blur(20px)',
                border: '1px solid rgba(255, 255, 255, 0.2)',
              }}
            >
              <Typography variant="h6" sx={{{ mb: 3, fontWeight: 600 }}>
                Ações Rápidas
              </Typography>
              <Box sx={{{ display: 'flex', flexDirection: 'column', gap: 2 }}>
                {quickActions.map((action, index) => (
                  <Button
                    key={index}}
                    variant="outlined"
                    onClick={action.action}}
                    sx={{
                      p: 2,
                      justifyContent: 'flex-start',
                      borderColor: 'rgba(0, 0, 0, 0.12)',
                      '&:hover': {
                        borderColor: action.color,
                        backgroundColor: `${action.color}08`,
                      },
                    }}
                  >
                    <Box
                      sx={{
                        p: 1,
                        borderRadius: 1,
                        backgroundColor: `${action.color}15`,
                        color: action.color,
                        mr: 2,
                      }}
                    >
                      {action.icon}}
                    </Box>
                    <Box sx={{{ textAlign: 'left' }}>
                      <Typography variant="subtitle2" sx={{{ fontWeight: 600 }}>
                        {action.title}}
                      </Typography>
                      <Typography variant="caption" color="text.secondary">
                        {action.description}}
                      </Typography>
                    </Box>
                  </Button>
                ))}}
              </Box>
            </Paper>
          </Grid>

          {/* Recent Projects */}}
          <Grid item xs={12} md={8}>
            <Paper
              component={motion.div}}
              initial={{ opacity: 0, x: 30 }}}
              animate={{ opacity: 1, x: 0 }}}
              transition={{ duration: 0.6, delay: 0.3 }}}
              sx={{
                p: 3,
                background: 'rgba(255, 255, 255, 0.95)',
                backdropFilter: 'blur(20px)',
                border: '1px solid rgba(255, 255, 255, 0.2)',
              }}
            >
              <Box sx={{{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 3 }}>
                <Typography variant="h6" sx={{{ fontWeight: 600 }}>
                  Projetos Recentes
                </Typography>
                <Button
                  variant="text"
                  onClick={() => navigate('/projects')}}
                  sx={{{ fontWeight: 600 }}}
                >
                  Ver todos
                </Button>
              </Box>
              
              <List>
                {recentProjects.map((project, index) => (
                  <React.Fragment key={index}>
                    <ListItem
                      sx={{
                        px: 0,
                        py: 2,
                        cursor: 'pointer',
                        borderRadius: 2,
                        '&:hover': {
                          backgroundColor: 'rgba(33, 150, 243, 0.04)',
                        },
                      }}
                      onClick={() => navigate(`/projects/${index + 1}`)}}
                    >
                      <ListItemIcon>
                        <Avatar
                          sx={{
                            bgcolor: 'primary.main',
                            width: 48,
                            height: 48,
                          }}
                        >
                          <PictureAsPdf />
                        </Avatar>
                      </ListItemIcon>
                      <ListItemText
                        primary={
                          <Box sx={{{ display: 'flex', alignItems: 'center', gap: 1 }}>
                            <Typography variant="subtitle1" sx={{{ fontWeight: 600 }}>
                              {project.name}}
                            </Typography>
                            <Chip
                              label={project.status}}
                              size="small"
                              color={project.status === 'Concluído' ? 'success' : 'warning'}}
                              icon={project.status === 'Concluído' ? <CheckCircle /> : <Schedule />}}
                            />
                          </Box>
                        }}
                        secondary={
                          <Box>
                            <Typography variant="body2" color="text.secondary">
                              {project.files} arquivos • {project.date}}
                            </Typography>
                            {project.status === 'Em andamento' && (
                              <LinearProgress
                                variant="determinate"
                                value={65}}
                                sx={{{ mt: 1, borderRadius: 1 }}}
                              />
                            )}}
                          </Box>
                        }}
                      />
                    </ListItem>
                    {index < recentProjects.length - 1 && <Divider />}}
                  </React.Fragment>
                ))}}
              </List>
            </Paper>
          </Grid>
        </Grid>
      </Box>
    </Container>
  );
};

export default DashboardPage;