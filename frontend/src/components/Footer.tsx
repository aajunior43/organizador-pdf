import React from 'react';
import {
  Box,
  Container,
  Typography,
  Link,
  Grid,
  IconButton,
  Divider,
} from '@mui/material';
import {
  GitHub,
  LinkedIn,
  Twitter,
  Email,
  Favorite,
} from '@mui/icons-material';
import { motion } from 'framer-motion';

const Footer: React.FC = () => {
  const currentYear = new Date().getFullYear();
  
  return (
    <Box
      component="footer"
      sx={{
        background: 'rgba(255, 255, 255, 0.95)',
        backdropFilter: 'blur(20px)',
        borderTop: '1px solid rgba(0, 0, 0, 0.1)',
        mt: 'auto',
      }}
    >
      <Container maxWidth="lg">
        <Box sx={{ py: 4 }}>
          <Grid container spacing={4}>
            {/* Logo and Description */}
            <Grid item xs={12} md={4}>
              <Box
                component={motion.div}
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.5 }}
              >
                <Typography
                  variant="h6"
                  component="div"
                  sx={{
                    fontWeight: 'bold',
                    background: 'linear-gradient(45deg, #2196F3, #21CBF3)',
                    backgroundClip: 'text',
                    WebkitBackgroundClip: 'text',
                    WebkitTextFillColor: 'transparent',
                    mb: 2,
                  }}
                >
                  📄 PDF Organizer
                </Typography>
                <Typography variant="body2" color="text.secondary" sx={{ mb: 2 }}>
                  A ferramenta mais moderna e intuitiva para organizar, mesclar e manipular seus arquivos PDF.
                  Interface responsiva, funcionalidades avançadas e experiência profissional.
                </Typography>
                <Box sx={{ display: 'flex', gap: 1 }}>
                  <IconButton
                    component={motion.div}
                    whileHover={{ scale: 1.1 }}
                    whileTap={{ scale: 0.9 }}
                    size="small"
                    href="https://github.com"
                    target="_blank"
                    rel="noopener noreferrer"
                  >
                    <GitHub />
                  </IconButton>
                  <IconButton
                    component={motion.div}
                    whileHover={{ scale: 1.1 }}
                    whileTap={{ scale: 0.9 }}
                    size="small"
                    href="https://linkedin.com"
                    target="_blank"
                    rel="noopener noreferrer"
                  >
                    <LinkedIn />
                  </IconButton>
                  <IconButton
                    component={motion.div}
                    whileHover={{ scale: 1.1 }}
                    whileTap={{ scale: 0.9 }}
                    size="small"
                    href="https://twitter.com"
                    target="_blank"
                    rel="noopener noreferrer"
                  >
                    <Twitter />
                  </IconButton>
                  <IconButton
                    component={motion.div}
                    whileHover={{ scale: 1.1 }}
                    whileTap={{ scale: 0.9 }}
                    size="small"
                    href="mailto:contato@pdforganizer.com"
                  >
                    <Email />
                  </IconButton>
                </Box>
              </Box>
            </Grid>
            
            {/* Quick Links */}
            <Grid item xs={12} sm={6} md={2}>
              <Box
                component={motion.div}
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.5, delay: 0.1 }}
              >
                <Typography variant="h6" sx={{ mb: 2, fontWeight: 600 }}>
                  Links Rápidos
                </Typography>
                <Box sx={{ display: 'flex', flexDirection: 'column', gap: 1 }}>
                  <Link href="/" color="text.secondary" underline="hover">
                    Início
                  </Link>
                  <Link href="/dashboard" color="text.secondary" underline="hover">
                    Dashboard
                  </Link>
                  <Link href="/projects" color="text.secondary" underline="hover">
                    Projetos
                  </Link>
                  <Link href="/docs" color="text.secondary" underline="hover">
                    Documentação
                  </Link>
                </Box>
              </Box>
            </Grid>
            
            {/* Features */}
            <Grid item xs={12} sm={6} md={3}>
              <Box
                component={motion.div}
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.5, delay: 0.2 }}
              >
                <Typography variant="h6" sx={{ mb: 2, fontWeight: 600 }}>
                  Funcionalidades
                </Typography>
                <Box sx={{ display: 'flex', flexDirection: 'column', gap: 1 }}>
                  <Typography variant="body2" color="text.secondary">
                    • Mesclagem de PDFs
                  </Typography>
                  <Typography variant="body2" color="text.secondary">
                    • Compressão inteligente
                  </Typography>
                  <Typography variant="body2" color="text.secondary">
                    • OCR avançado
                  </Typography>
                  <Typography variant="body2" color="text.secondary">
                    • Marca d'água
                  </Typography>
                  <Typography variant="body2" color="text.secondary">
                    • Assinatura digital
                  </Typography>
                </Box>
              </Box>
            </Grid>
            
            {/* Support */}
            <Grid item xs={12} md={3}>
              <Box
                component={motion.div}
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.5, delay: 0.3 }}
              >
                <Typography variant="h6" sx={{ mb: 2, fontWeight: 600 }}>
                  Suporte
                </Typography>
                <Box sx={{ display: 'flex', flexDirection: 'column', gap: 1 }}>
                  <Link href="/help" color="text.secondary" underline="hover">
                    Central de Ajuda
                  </Link>
                  <Link href="/contact" color="text.secondary" underline="hover">
                    Contato
                  </Link>
                  <Link href="/privacy" color="text.secondary" underline="hover">
                    Privacidade
                  </Link>
                  <Link href="/terms" color="text.secondary" underline="hover">
                    Termos de Uso
                  </Link>
                </Box>
              </Box>
            </Grid>
          </Grid>
          
          <Divider sx={{ my: 3 }} />
          
          {/* Copyright */}
          <Box
            component={motion.div}
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ duration: 0.5, delay: 0.4 }}
            sx={{
              display: 'flex',
              flexDirection: { xs: 'column', sm: 'row' },
              justifyContent: 'space-between',
              alignItems: 'center',
              gap: 2,
            }}
          >
            <Typography variant="body2" color="text.secondary">
              © {currentYear} PDF Organizer. Todos os direitos reservados.
            </Typography>
            <Box sx={{ display: 'flex', alignItems: 'center', gap: 0.5 }}>
              <Typography variant="body2" color="text.secondary">
                Feito com
              </Typography>
              <Favorite sx={{ color: 'red', fontSize: 16 }} />
              <Typography variant="body2" color="text.secondary">
                para facilitar seu trabalho
              </Typography>
            </Box>
          </Box>
        </Box>
      </Container>
    </Box>
  );
};

export default Footer;