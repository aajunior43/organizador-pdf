import React, { useState } from 'react';
import {
  Container,
  Paper,
  Typography,
  Box,
  Switch,
  FormControlLabel,
  Divider,
  Button,
  Alert,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  TextField,
  Select,
  MenuItem,
  FormControl,
  InputLabel,
  Card,
  CardContent,
  CardHeader,
  List,
  ListItem,
  ListItemText,
  ListItemSecondaryAction,
  IconButton,
  Chip,
} from '@mui/material';
import { motion } from 'framer-motion';
import {
  Notifications as NotificationsIcon,
  Security as SecurityIcon,
  Palette as PaletteIcon,
  Language as LanguageIcon,
  Storage as StorageIcon,
  Delete as DeleteIcon,
  Download as DownloadIcon,
  CloudSync as CloudSyncIcon,
  Speed as SpeedIcon,
} from '@mui/icons-material';
import { useAuthStore } from '../store/authStore';

interface SettingsState {
  notifications: {
    email: boolean;
    push: boolean;
    desktop: boolean;
    projectUpdates: boolean;
    securityAlerts: boolean;
  };
  appearance: {
    theme: 'light' | 'dark' | 'auto';
    language: string;
    compactMode: boolean;
  };
  privacy: {
    profileVisibility: 'public' | 'private';
    dataCollection: boolean;
    analytics: boolean;
  };
  performance: {
    autoSave: boolean;
    preloadImages: boolean;
    compressionLevel: number;
  };
}

const SettingsPage: React.FC = () => {
  const { user, logout } = useAuthStore();
  const [settings, setSettings] = useState<SettingsState>({
    notifications: {
      email: true,
      push: true,
      desktop: false,
      projectUpdates: true,
      securityAlerts: true,
    },
    appearance: {
      theme: 'auto',
      language: 'pt-BR',
      compactMode: false,
    },
    privacy: {
      profileVisibility: 'private',
      dataCollection: true,
      analytics: false,
    },
    performance: {
      autoSave: true,
      preloadImages: true,
      compressionLevel: 85,
    },
  });

  const [deleteDialogOpen, setDeleteDialogOpen] = useState(false);
  const [exportDialogOpen, setExportDialogOpen] = useState(false);
  const [saveSuccess, setSaveSuccess] = useState(false);

  const handleSettingChange = (category: keyof SettingsState, key: string, value: any) => {
    setSettings(prev => ({
      ...prev,
      [category]: {
        ...prev[category],
        [key]: value,
      },
    }));
  };

  const handleSaveSettings = async () => {
    try {
      // Save settings to backend
      console.log('Saving settings:', settings);
      setSaveSuccess(true);
      setTimeout(() => setSaveSuccess(false), 3000);
    } catch (error) {
      console.error('Error saving settings:', error);
    }
  };

  const handleExportData = () => {
    // Export user data
    const dataToExport = {
      user,
      settings,
      exportDate: new Date().toISOString(),
    };
    
    const blob = new Blob([JSON.stringify(dataToExport, null, 2)], {
      type: 'application/json',
    });
    
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `pdf-organizer-data-${new Date().toISOString().split('T')[0]}.json`;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
    
    setExportDialogOpen(false);
  };

  const handleDeleteAccount = async () => {
    try {
      // Delete account logic
      console.log('Deleting account...');
      await logout();
      setDeleteDialogOpen(false);
    } catch (error) {
      console.error('Error deleting account:', error);
    }
  };

  const clearCache = () => {
    if ('caches' in window) {
      caches.keys().then(names => {
        names.forEach(name => {
          caches.delete(name);
        });
      });
    }
    localStorage.clear();
    sessionStorage.clear();
    window.location.reload();
  };

  return (
    <Container maxWidth="md" sx={{ py: 4 }}>
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5 }}
      >
        <Typography
          variant="h4"
          component="h1"
          gutterBottom
          sx={{
            fontWeight: 'bold',
            color: 'white',
            textAlign: 'center',
            mb: 4,
          }}
        >
          Configurações
        </Typography>

        {saveSuccess && (
          <motion.div
            initial={{ opacity: 0, y: -20 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: -20 }}
          >
            <Alert severity="success" sx={{ mb: 3 }}>
              Configurações salvas com sucesso!
            </Alert>
          </motion.div>
        )}

        {/* Notifications Settings */}
        <Card sx={{ mb: 3 }}>
          <CardHeader
            avatar={<NotificationsIcon color="primary" />}
            title="Notificações"
            subheader="Gerencie como você recebe notificações"
          />
          <CardContent>
            <List>
              <ListItem>
                <ListItemText
                  primary="Notificações por Email"
                  secondary="Receba atualizações importantes por email"
                />
                <ListItemSecondaryAction>
                  <Switch
                    checked={settings.notifications.email}
                    onChange={(e) => handleSettingChange('notifications', 'email', e.target.checked)}
                  />
                </ListItemSecondaryAction>
              </ListItem>
              
              <ListItem>
                <ListItemText
                  primary="Notificações Push"
                  secondary="Receba notificações push no navegador"
                />
                <ListItemSecondaryAction>
                  <Switch
                    checked={settings.notifications.push}
                    onChange={(e) => handleSettingChange('notifications', 'push', e.target.checked)}
                  />
                </ListItemSecondaryAction>
              </ListItem>
              
              <ListItem>
                <ListItemText
                  primary="Atualizações de Projetos"
                  secondary="Notificações sobre progresso dos seus projetos"
                />
                <ListItemSecondaryAction>
                  <Switch
                    checked={settings.notifications.projectUpdates}
                    onChange={(e) => handleSettingChange('notifications', 'projectUpdates', e.target.checked)}
                  />
                </ListItemSecondaryAction>
              </ListItem>
            </List>
          </CardContent>
        </Card>

        {/* Appearance Settings */}
        <Card sx={{ mb: 3 }}>
          <CardHeader
            avatar={<PaletteIcon color="primary" />}
            title="Aparência"
            subheader="Personalize a interface do aplicativo"
          />
          <CardContent>
            <Box sx={{ display: 'flex', flexDirection: 'column', gap: 3 }}>
              <FormControl fullWidth>
                <InputLabel>Tema</InputLabel>
                <Select
                  value={settings.appearance.theme}
                  label="Tema"
                  onChange={(e) => handleSettingChange('appearance', 'theme', e.target.value)}
                >
                  <MenuItem value="light">Claro</MenuItem>
                  <MenuItem value="dark">Escuro</MenuItem>
                  <MenuItem value="auto">Automático</MenuItem>
                </Select>
              </FormControl>
              
              <FormControl fullWidth>
                <InputLabel>Idioma</InputLabel>
                <Select
                  value={settings.appearance.language}
                  label="Idioma"
                  onChange={(e) => handleSettingChange('appearance', 'language', e.target.value)}
                >
                  <MenuItem value="pt-BR">Português (Brasil)</MenuItem>
                  <MenuItem value="en-US">English (US)</MenuItem>
                  <MenuItem value="es-ES">Español</MenuItem>
                  <MenuItem value="fr-FR">Français</MenuItem>
                </Select>
              </FormControl>
              
              <FormControlLabel
                control={
                  <Switch
                    checked={settings.appearance.compactMode}
                    onChange={(e) => handleSettingChange('appearance', 'compactMode', e.target.checked)}
                  />
                }
                label="Modo Compacto"
              />
            </Box>
          </CardContent>
        </Card>

        {/* Performance Settings */}
        <Card sx={{ mb: 3 }}>
          <CardHeader
            avatar={<SpeedIcon color="primary" />}
            title="Performance"
            subheader="Otimize a performance do aplicativo"
          />
          <CardContent>
            <Box sx={{ display: 'flex', flexDirection: 'column', gap: 3 }}>
              <FormControlLabel
                control={
                  <Switch
                    checked={settings.performance.autoSave}
                    onChange={(e) => handleSettingChange('performance', 'autoSave', e.target.checked)}
                  />
                }
                label="Salvamento Automático"
              />
              
              <FormControlLabel
                control={
                  <Switch
                    checked={settings.performance.preloadImages}
                    onChange={(e) => handleSettingChange('performance', 'preloadImages', e.target.checked)}
                  />
                }
                label="Pré-carregar Imagens"
              />
              
              <Box>
                <Typography gutterBottom>Nível de Compressão: {settings.performance.compressionLevel}%</Typography>
                <input
                  type="range"
                  min="50"
                  max="100"
                  value={settings.performance.compressionLevel}
                  onChange={(e) => handleSettingChange('performance', 'compressionLevel', parseInt(e.target.value))}
                  style={{ width: '100%' }}
                />
              </Box>
            </Box>
          </CardContent>
        </Card>

        {/* Privacy Settings */}
        <Card sx={{ mb: 3 }}>
          <CardHeader
            avatar={<SecurityIcon color="primary" />}
            title="Privacidade e Segurança"
            subheader="Controle seus dados e privacidade"
          />
          <CardContent>
            <Box sx={{ display: 'flex', flexDirection: 'column', gap: 3 }}>
              <FormControl fullWidth>
                <InputLabel>Visibilidade do Perfil</InputLabel>
                <Select
                  value={settings.privacy.profileVisibility}
                  label="Visibilidade do Perfil"
                  onChange={(e) => handleSettingChange('privacy', 'profileVisibility', e.target.value)}
                >
                  <MenuItem value="public">Público</MenuItem>
                  <MenuItem value="private">Privado</MenuItem>
                </Select>
              </FormControl>
              
              <FormControlLabel
                control={
                  <Switch
                    checked={settings.privacy.dataCollection}
                    onChange={(e) => handleSettingChange('privacy', 'dataCollection', e.target.checked)}
                  />
                }
                label="Permitir Coleta de Dados para Melhorias"
              />
              
              <FormControlLabel
                control={
                  <Switch
                    checked={settings.privacy.analytics}
                    onChange={(e) => handleSettingChange('privacy', 'analytics', e.target.checked)}
                  />
                }
                label="Analytics e Métricas de Uso"
              />
            </Box>
          </CardContent>
        </Card>

        {/* Data Management */}
        <Card sx={{ mb: 3 }}>
          <CardHeader
            avatar={<StorageIcon color="primary" />}
            title="Gerenciamento de Dados"
            subheader="Exporte ou limpe seus dados"
          />
          <CardContent>
            <Box sx={{ display: 'flex', flexDirection: 'column', gap: 2 }}>
              <Button
                variant="outlined"
                startIcon={<DownloadIcon />}
                onClick={() => setExportDialogOpen(true)}
                fullWidth
              >
                Exportar Meus Dados
              </Button>
              
              <Button
                variant="outlined"
                startIcon={<DeleteIcon />}
                onClick={clearCache}
                fullWidth
              >
                Limpar Cache Local
              </Button>
            </Box>
          </CardContent>
        </Card>

        {/* Save Button */}
        <Box sx={{ display: 'flex', gap: 2, justifyContent: 'center', mb: 3 }}>
          <Button
            variant="contained"
            size="large"
            onClick={handleSaveSettings}
            sx={{ px: 4 }}
          >
            Salvar Configurações
          </Button>
        </Box>

        {/* Danger Zone */}
        <Card sx={{ border: '1px solid', borderColor: 'error.main' }}>
          <CardHeader
            title="Zona de Perigo"
            subheader="Ações irreversíveis"
            sx={{ color: 'error.main' }}
          />
          <CardContent>
            <Button
              variant="outlined"
              color="error"
              startIcon={<DeleteIcon />}
              onClick={() => setDeleteDialogOpen(true)}
              fullWidth
            >
              Excluir Conta Permanentemente
            </Button>
          </CardContent>
        </Card>
      </motion.div>

      {/* Delete Account Dialog */}
      <Dialog open={deleteDialogOpen} onClose={() => setDeleteDialogOpen(false)}>
        <DialogTitle>Excluir Conta</DialogTitle>
        <DialogContent>
          <Typography>
            Tem certeza de que deseja excluir sua conta permanentemente?
            Esta ação não pode ser desfeita e todos os seus dados serão perdidos.
          </Typography>
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setDeleteDialogOpen(false)}>Cancelar</Button>
          <Button onClick={handleDeleteAccount} color="error" variant="contained">
            Excluir Permanentemente
          </Button>
        </DialogActions>
      </Dialog>

      {/* Export Data Dialog */}
      <Dialog open={exportDialogOpen} onClose={() => setExportDialogOpen(false)}>
        <DialogTitle>Exportar Dados</DialogTitle>
        <DialogContent>
          <Typography>
            Seus dados serão exportados em formato JSON incluindo:
          </Typography>
          <List dense>
            <ListItem>
              <ListItemText primary="• Informações do perfil" />
            </ListItem>
            <ListItem>
              <ListItemText primary="• Configurações do aplicativo" />
            </ListItem>
            <ListItem>
              <ListItemText primary="• Histórico de projetos" />
            </ListItem>
          </List>
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setExportDialogOpen(false)}>Cancelar</Button>
          <Button onClick={handleExportData} variant="contained">
            Exportar
          </Button>
        </DialogActions>
      </Dialog>
    </Container>
  );
};

export default SettingsPage;