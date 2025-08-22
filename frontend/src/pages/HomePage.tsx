import React from 'react';
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
  useTheme,
  useMediaQuery,
} from '@mui/material';
import {
  PictureAsPdf,
  MergeType,
  Compress,
  Security,
  CloudUpload,
  Speed,
  Devices,
  CheckCircle,
  ArrowForward,
  GetApp,
} from '@mui/icons-material';
import { motion } from 'framer-motion';
import { useNavigate } from 'react-router-dom';
import { useAuthStore } from '../store/authStore';

const HomePage: React.FC = () => {
  const navigate = useNavigate();
  const theme = useTheme();
  const isMobile = useMediaQuery(theme.breakpoints.down('md'));
  const { isAuthenticated } = useAuthStore();

  const features = [
    {
      icon: <MergeType sx={{ fontSize: 40 }} />,
      title: 'Mesclagem Inteligente',
      description: 'Combine múltiplos PDFs em um único arquivo com ordem personalizada e preview em tempo real.',
      color: '#2196F3',
    },
    {
      icon: <Compress sx={{ fontSize: 40 }} />,
      title: 'Compressão Avançada',
      description: 'Reduza o tamanho dos seus PDFs mantendo a qualidade com algoritmos de compressão inteligentes.',
      color: '#4CAF50',
    },
    {
      icon: <Security sx={{ fontSize: 40 }} />,
      title: 'OCR e Segurança',
      description: 'Extraia texto com OCR, adicione marcas d\'água e assinaturas digitais para proteger seus documentos.',
      color: '#FF9800',
    },
    {
      icon: <CloudUpload sx={{ fontSize: 40 }} />,
      title: 'Upload em Lote',
      description: 'Faça upload de múltiplos arquivos simultaneamente com barra de progresso e preview instantâneo.',
      color: '#9C27B0',
    },
    {
      icon: <Speed sx={{ fontSize: 40 }} />,
      title: 'Processamento Rápido',
      description: 'Engine otimizada para processamento rápido de arquivos grandes com feedback em tempo real.',
      color: '#F44336',
    },
    {
      icon: <Devices sx={{ fontSize: 40 }} />,
      title: 'Totalmente Responsivo',
      description: 'Interface moderna que funciona perfeitamente em desktop, tablet e dispositivos móveis.',
      color: '#00BCD4',
    },
  ];

  const stats = [
    { number: '10K+', label: 'PDFs Processados' },
    { number: '500+', label: 'Usuários Ativos' },
    { number: '99.9%', label: 'Uptime' },
    { number: '24/7', label: 'Suporte' },
  ];

  return (
    <Box>
      {/* Hero Section */}
      <Container maxWidth="lg">
        <Box
          sx={
            minHeight: '80vh',
            display: 'flex',
            alignItems: 'center',
            py: { xs: 4, md: 8 },
          }
        >
          <Grid container spacing={4} alignItems="center">
            <Grid item xs={12} md={6}>
              <Box
                component={motion.div}
                initial={{ opacity: 0, x: -50 }}
                animate={{ opacity: 1, x: 0 }}
                transition={{ duration: 0.8 }}
              >
                <Typography
                  variant="h1"
                  sx={
                    fontSize: { xs: '2.5rem', md: '3.5rem', lg: '4rem' },
                    fontWeight: 700,
                    mb: 2,
                    background: 'linear-gradient(45deg, #2196F3, #21CBF3)',
                    backgroundClip: 'text',
                    WebkitBackgroundClip: 'text',
                    WebkitTextFillColor: 'transparent',
                  }
                >
                  Organize seus PDFs
                  <br />
                  como nunca antes
                </Typography>
                
                <Typography
                  variant="h5"
                  sx={
                    mb: 4,
                    color: 'rgba(255, 255, 255, 0.9)',
                    fontWeight: 400,
                    lineHeight: 1.6,
                  }
                >
                  A ferramenta mais moderna e intuitiva para mesclar, organizar e manipular
                  seus arquivos PDF. Interface responsiva, funcionalidades avançadas e
                  experiência profissional.
                </Typography>
                
                <Box sx={{ display: 'flex', gap: 2, flexWrap: 'wrap' }}>
                  <Button
                    variant="contained"
                    size="large"
                    onClick={() => navigate(isAuthenticated ? '/dashboard' : '/register')}
                    sx={
                      px: 4,
                      py: 1.5,
                      fontSize: '1.1rem',
                      fontWeight: 600,
                      background: 'linear-gradient(45deg, #2196F3, #21CBF3)',
                      '&:hover': {
                        background: 'linear-gradient(45deg, #1976D2, #1CB5E0)',
                        transform: 'translateY(-2px)',
                      },
                      transition: 'all 0.3s ease',
                    }
                    endIcon={<ArrowForward />}
                  >
                    {isAuthenticated ? 'Ir para Dashboard' : 'Começar Agora'}
                  </Button>
                  
                  <Button
                    variant="outlined"
                    size="large"
                    onClick={() => navigate('/demo')}
                    sx={
                      px: 4,
                      py: 1.5,
                      fontSize: '1.1rem',
                      fontWeight: 600,
                      borderColor: 'rgba(255, 255, 255, 0.5)',
                      color: 'white',
                      '&:hover': {
                        borderColor: 'white',
                        backgroundColor: 'rgba(255, 255, 255, 0.1)',
                        transform: 'translateY(-2px)',
                      },
                      transition: 'all 0.3s ease',
                    }
                    endIcon={<GetApp />}
                  >
                    Ver Demo
                  </Button>
                </Box>
                
                <Box sx={{ mt: 4, display: 'flex', gap: 2, flexWrap: 'wrap' }}>
                  <Chip
                    icon={<CheckCircle />}
                    label="Gratuito para começar"
                    sx={
                      backgroundColor: 'rgba(255, 255, 255, 0.2)',
                      color: 'white',
                      '& .MuiChip-icon': { color: '#4CAF50' },
                    }
                  />
                  <Chip
                    icon={<CheckCircle />}
                    label="Sem instalação"
                    sx={
                      backgroundColor: 'rgba(255, 255, 255, 0.2)',
                      color: 'white',
                      '& .MuiChip-icon': { color: '#4CAF50' },
                    }
                  />
                  <Chip
                    icon={<CheckCircle />}
                    label="100% seguro"
                    sx={
                      backgroundColor: 'rgba(255, 255, 255, 0.2)',
                      color: 'white',
                      '& .MuiChip-icon': { color: '#4CAF50' },
                    }
                  />
                </Box>
              </Box>
            </Grid>
            
            <Grid item xs={12} md={6}>
              <Box
                component={motion.div}
                initial={{ opacity: 0, x: 50 }}
                animate={{ opacity: 1, x: 0 }}
                transition={{ duration: 0.8, delay: 0.2 }}
                sx={
                  display: 'flex',
                  justifyContent: 'center',
                  alignItems: 'center',
                }
              >
                <Paper
                  elevation={20}
                  sx={
                    p: 4,
                    borderRadius: 4,
                    background: 'rgba(255, 255, 255, 0.95)',
                    backdropFilter: 'blur(20px)',
                    border: '1px solid rgba(255, 255, 255, 0.2)',
                    maxWidth: 400,
                    width: '100%',
                  }
                >
                  <Box sx={{ textAlign: 'center' }}>
                    <PictureAsPdf sx={{ fontSize: 80, color: 'primary.main', mb: 2 }} />
                    <Typography variant="h6" sx={{ mb: 2, fontWeight: 600 }}>
                      Interface Moderna
                    </Typography>
                    <Typography variant="body2" color="text.secondary">
                      Design intuitivo e responsivo para uma experiência excepcional
                      em qualquer dispositivo.
                    </Typography>
                  </Box>
                </Paper>
              </Box>
            </Grid>
          </Grid>
        </Box>
      </Container>

      {/* Stats Section */}
      <Box sx={{ py: 8, backgroundColor: 'rgba(255, 255, 255, 0.1)' }}>
        <Container maxWidth="lg">
          <Grid container spacing={4}>
            {stats.map((stat, index) => (
              <Grid item xs={6} md={3} key={index}>
                <Box
                  component={motion.div}
                  initial={{ opacity: 0, y: 30 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ duration: 0.6, delay: index * 0.1 }}
                  sx={{ textAlign: 'center' }}
                >
                  <Typography
                    variant="h3"
                    sx={
                      fontWeight: 700,
                      color: 'white',
                      mb: 1,
                    }
                  >
                    {stat.number}
                  </Typography>
                  <Typography
                    variant="body1"
                    sx={
                      color: 'rgba(255, 255, 255, 0.8)',
                      fontWeight: 500,
                    }
                  >
                    {stat.label}
                  </Typography>
                </Box>
              </Grid>
            ))}
          </Grid>
        </Container>
      </Box>

      {/* Features Section */}
      <Box sx={{ py: 8, backgroundColor: 'rgba(255, 255, 255, 0.95)' }}>
        <Container maxWidth="lg">
          <Box sx={{ textAlign: 'center', mb: 6 }}>
            <Typography
              variant="h2"
              sx={
                fontSize: { xs: '2rem', md: '2.5rem' },
                fontWeight: 700,
                mb: 2,
                color: 'text.primary',
              }
            >
              Funcionalidades Poderosas
            </Typography>
            <Typography
              variant="h6"
              sx={
                color: 'text.secondary',
                maxWidth: 600,
                mx: 'auto',
              }
            >
              Tudo que você precisa para trabalhar com PDFs de forma profissional
              e eficiente.
            </Typography>
          </Box>
          
          <Grid container spacing={4}>
            {features.map((feature, index) => (
              <Grid item xs={12} md={6} lg={4} key={index}>
                <Card
                  component={motion.div}
                  initial={{ opacity: 0, y: 30 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ duration: 0.6, delay: index * 0.1 }}
                  whileHover={{ y: -8, transition: { duration: 0.3 } }}
                  sx={
                    height: '100%',
                    display: 'flex',
                    flexDirection: 'column',
                    '&:hover': {
                      boxShadow: '0 12px 40px rgba(0,0,0,0.15)',
                    },
                    transition: 'all 0.3s ease',
                  }
                >
                  <CardContent sx={{ flexGrow: 1, p: 3 }}>
                    <Box
                      sx={
                        display: 'flex',
                        alignItems: 'center',
                        mb: 2,
                        color: feature.color,
                      }
                    >
                      {feature.icon}
                    </Box>
                    <Typography
                      variant="h6"
                      sx={{ mb: 2, fontWeight: 600 }}
                    >
                      {feature.title}
                    </Typography>
                    <Typography
                      variant="body2"
                      color="text.secondary"
                      sx={{ lineHeight: 1.6 }}
                    >
                      {feature.description}
                    </Typography>
                  </CardContent>
                </Card>
              </Grid>
            ))}
          </Grid>
        </Container>
      </Box>

      {/* CTA Section */}
      <Box sx={{ py: 8, backgroundColor: 'rgba(255, 255, 255, 0.1)' }}>
        <Container maxWidth="md">
          <Box
            component={motion.div}
            initial={{ opacity: 0, y: 30 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.8 }}
            sx={{ textAlign: 'center' }}
          >
            <Typography
              variant="h3"
              sx={
                fontSize: { xs: '1.8rem', md: '2.5rem' },
                fontWeight: 700,
                mb: 2,
                color: 'white',
              }
            >
              Pronto para começar?
            </Typography>
            <Typography
              variant="h6"
              sx={
                mb: 4,
                color: 'rgba(255, 255, 255, 0.9)',
                maxWidth: 500,
                mx: 'auto',
              }
            >
              Junte-se a milhares de usuários que já descobriram a forma mais
              eficiente de trabalhar com PDFs.
            </Typography>
            <Button
              variant="contained"
              size="large"
              onClick={() => navigate(isAuthenticated ? '/dashboard' : '/register')}
              sx={
                px: 6,
                py: 2,
                fontSize: '1.2rem',
                fontWeight: 600,
                background: 'linear-gradient(45deg, #2196F3, #21CBF3)',
                '&:hover': {
                  background: 'linear-gradient(45deg, #1976D2, #1CB5E0)',
                  transform: 'translateY(-3px)',
                },
                transition: 'all 0.3s ease',
              }
              endIcon={<ArrowForward />}
            >
              {isAuthenticated ? 'Acessar Dashboard' : 'Criar Conta Gratuita'}
            </Button>
          </Box>
        </Container>
      </Box>
    </Box>
  );
};

export default HomePage;