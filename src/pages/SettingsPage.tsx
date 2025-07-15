import React, { useState, useEffect } from "react";
import {
  ArrowLeft,
  User,
  Bell,
  Shield,
  Palette,
  Globe,
  Download,
  Trash2,
  Key,
  Eye,
  Users,
  Lock,
  Camera,
  Mail,
  Phone,
  MapPin,
  Calendar,
  Briefcase,
  GraduationCap,
  Heart,
  Link as LinkIcon,
  Save,
  Check,
} from "lucide-react";
import { useNavigate } from "react-router-dom";

interface User {
  id?: number;
  display_id?: string;
  name: string;
  email: string;
  avatar?: string;
  cover_photo?: string;
  bio?: string;
  location?: string;
  username?: string;
  nickname?: string;
  phone?: string;
  website?: string;
  birth_date?: string;
  gender?: string;
  relationship_status?: string;
  work?: string;
  education?: string;
  token: string;
}

interface SettingsPageProps {
  user: User;
  onLogout: () => void;
  onUserUpdate?: (userData: Partial<User>) => void;
}

export function SettingsPage({
  user,
  onLogout,
  onUserUpdate,
}: SettingsPageProps) {
  const navigate = useNavigate();
  const [activeSection, setActiveSection] = useState("profile");
  const [loading, setLoading] = useState(false);
  const [saved, setSaved] = useState(false);

  // Profile data
  const [profileData, setProfileData] = useState({
    first_name: user.name.split(" ")[0] || "",
    last_name: user.name.split(" ").slice(1).join(" ") || "",
    username: user.username || "",
    nickname: user.nickname || "",
    bio: user.bio || "",
    email: user.email || "",
    phone: user.phone || "",
    website: user.website || "",
    location: user.location || "",
    work: user.work || "",
    education: user.education || "",
    birth_date: user.birth_date || "",
    gender: user.gender || "",
    relationship_status: user.relationship_status || "",
  });

  // Privacy settings
  const [privacySettings, setPrivacySettings] = useState({
    profile_visibility: "friends",
    post_visibility: "friends",
    story_visibility: "friends",
    friend_requests: "everyone",
    tagging_permission: "friends",
    email_visibility: "private",
    phone_visibility: "private",
    birth_date_visibility: "friends",
  });

  // Notification settings
  const [notificationSettings, setNotificationSettings] = useState({
    email_notifications: true,
    push_notifications: true,
    friend_request_notifications: true,
    comment_notifications: true,
    reaction_notifications: true,
    message_notifications: true,
    story_notifications: true,
  });

  useEffect(() => {
    fetchPrivacySettings();
    fetchNotificationSettings();
  }, []);

  const fetchPrivacySettings = async () => {
    try {
      const response = await fetch("http://localhost:8000/settings/privacy", {
        headers: { Authorization: `Bearer ${user.token}` },
      });
      if (response.ok) {
        const data = await response.json();
        setPrivacySettings(data);
      }
    } catch (error) {
      console.error("Erro ao buscar configurações de privacidade:", error);
    }
  };

  const fetchNotificationSettings = async () => {
    try {
      const response = await fetch(
        "http://localhost:8000/settings/notifications",
        {
          headers: { Authorization: `Bearer ${user.token}` },
        },
      );
      if (response.ok) {
        const data = await response.json();
        setNotificationSettings(data);
      }
    } catch (error) {
      console.error("Erro ao buscar configurações de notificação:", error);
    }
  };

  const handleSaveProfile = async () => {
    setLoading(true);
    try {
      const response = await fetch("http://localhost:8000/settings/profile", {
        method: "PUT",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${user.token}`,
        },
        body: JSON.stringify(profileData),
      });

      if (response.ok) {
        setSaved(true);
        setTimeout(() => setSaved(false), 2000);
        if (onUserUpdate) {
          onUserUpdate({
            name: `${profileData.first_name} ${profileData.last_name}`,
            username: profileData.username,
            nickname: profileData.nickname,
            bio: profileData.bio,
            phone: profileData.phone,
            website: profileData.website,
            location: profileData.location,
            work: profileData.work,
            education: profileData.education,
            birth_date: profileData.birth_date,
            gender: profileData.gender,
            relationship_status: profileData.relationship_status,
          });
        }
      }
    } catch (error) {
      console.error("Erro ao salvar perfil:", error);
    } finally {
      setLoading(false);
    }
  };

  const handleSavePrivacy = async () => {
    setLoading(true);
    try {
      const response = await fetch("http://localhost:8000/settings/privacy", {
        method: "PUT",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${user.token}`,
        },
        body: JSON.stringify(privacySettings),
      });

      if (response.ok) {
        setSaved(true);
        setTimeout(() => setSaved(false), 2000);
      }
    } catch (error) {
      console.error("Erro ao salvar configurações de privacidade:", error);
    } finally {
      setLoading(false);
    }
  };

  const handleSaveNotifications = async () => {
    setLoading(true);
    try {
      const response = await fetch(
        "http://localhost:8000/settings/notifications",
        {
          method: "PUT",
          headers: {
            "Content-Type": "application/json",
            Authorization: `Bearer ${user.token}`,
          },
          body: JSON.stringify(notificationSettings),
        },
      );

      if (response.ok) {
        setSaved(true);
        setTimeout(() => setSaved(false), 2000);
      }
    } catch (error) {
      console.error("Erro ao salvar configurações de notificação:", error);
    } finally {
      setLoading(false);
    }
  };

  const sections = [
    { id: "profile", label: "Perfil", icon: User },
    { id: "privacy", label: "Privacidade", icon: Shield },
    { id: "notifications", label: "Notificações", icon: Bell },
    { id: "appearance", label: "Aparência", icon: Palette },
    { id: "language", label: "Idioma", icon: Globe },
    { id: "data", label: "Dados", icon: Download },
    { id: "account", label: "Conta", icon: Trash2 },
  ];

  const renderProfileSection = () => (
    <div className="space-y-8">
      <div>
        <h2 className="text-2xl font-bold text-gray-900 mb-2">
          Informações do Perfil
        </h2>
        <p className="text-gray-600">
          Gerencie suas informações pessoais e como outros te veem
        </p>
      </div>

      <div className="bg-white p-6 rounded-xl shadow-sm border">
        <h3 className="text-lg font-semibold text-gray-900 mb-4">
          Informações Básicas
        </h3>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Nome
            </label>
            <input
              type="text"
              value={profileData.first_name}
              onChange={(e) =>
                setProfileData((prev) => ({
                  ...prev,
                  first_name: e.target.value,
                }))
              }
              className="w-full p-3 border border-gray-300 rounded-xl focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            />
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Sobrenome
            </label>
            <input
              type="text"
              value={profileData.last_name}
              onChange={(e) =>
                setProfileData((prev) => ({
                  ...prev,
                  last_name: e.target.value,
                }))
              }
              className="w-full p-3 border border-gray-300 rounded-xl focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            />
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Nome de usuário
            </label>
            <input
              type="text"
              value={profileData.username}
              onChange={(e) =>
                setProfileData((prev) => ({
                  ...prev,
                  username: e.target.value,
                }))
              }
              className="w-full p-3 border border-gray-300 rounded-xl focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            />
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Apelido
            </label>
            <input
              type="text"
              value={profileData.nickname}
              onChange={(e) =>
                setProfileData((prev) => ({
                  ...prev,
                  nickname: e.target.value,
                }))
              }
              className="w-full p-3 border border-gray-300 rounded-xl focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            />
          </div>
        </div>
      </div>

      <div className="flex justify-end">
        <button
          onClick={handleSaveProfile}
          disabled={loading}
          className="flex items-center space-x-2 bg-blue-600 hover:bg-blue-700 disabled:bg-blue-400 text-white px-6 py-3 rounded-xl font-medium transition-colors"
        >
          {saved ? <Check className="w-5 h-5" /> : <Save className="w-5 h-5" />}
          <span>
            {saved ? "Salvo!" : loading ? "Salvando..." : "Salvar Alterações"}
          </span>
        </button>
      </div>
    </div>
  );

  const renderPrivacySection = () => (
    <div className="space-y-8">
      <div>
        <h2 className="text-2xl font-bold text-gray-900 mb-2">
          Configurações de Privacidade
        </h2>
        <p className="text-gray-600">
          Controle quem pode ver seu conteúdo e interagir com você
        </p>
      </div>

      <div className="bg-white p-6 rounded-xl shadow-sm border">
        <h3 className="text-lg font-semibold text-gray-900 mb-4">
          Visibilidade do Perfil
        </h3>
        <div className="space-y-4">
          {[
            {
              key: "profile_visibility",
              label: "Quem pode ver seu perfil",
              icon: Eye,
            },
            {
              key: "post_visibility",
              label: "Quem pode ver seus posts",
              icon: Globe,
            },
            {
              key: "story_visibility",
              label: "Quem pode ver suas stories",
              icon: Camera,
            },
          ].map(({ key, label, icon: Icon }) => (
            <div key={key} className="flex items-center justify-between">
              <div className="flex items-center space-x-3">
                <Icon className="w-5 h-5 text-gray-500" />
                <span className="text-gray-700">{label}</span>
              </div>
              <select
                value={privacySettings[key as keyof typeof privacySettings]}
                onChange={(e) =>
                  setPrivacySettings((prev) => ({
                    ...prev,
                    [key]: e.target.value,
                  }))
                }
                className="border border-gray-300 rounded-lg px-3 py-2 focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              >
                <option value="public">Público</option>
                <option value="friends">Amigos</option>
                <option value="private">Apenas eu</option>
              </select>
            </div>
          ))}
        </div>
      </div>

      <div className="flex justify-end">
        <button
          onClick={handleSavePrivacy}
          disabled={loading}
          className="flex items-center space-x-2 bg-blue-600 hover:bg-blue-700 disabled:bg-blue-400 text-white px-6 py-3 rounded-xl font-medium transition-colors"
        >
          {saved ? <Check className="w-5 h-5" /> : <Save className="w-5 h-5" />}
          <span>
            {saved ? "Salvo!" : loading ? "Salvando..." : "Salvar Alterações"}
          </span>
        </button>
      </div>
    </div>
  );

  const renderNotificationsSection = () => (
    <div className="space-y-8">
      <div>
        <h2 className="text-2xl font-bold text-gray-900 mb-2">Notificações</h2>
        <p className="text-gray-600">
          Gerencie como e quando você recebe notificações
        </p>
      </div>

      <div className="bg-white p-6 rounded-xl shadow-sm border">
        <h3 className="text-lg font-semibold text-gray-900 mb-4">
          Notificações Push
        </h3>
        <div className="space-y-4">
          {[
            {
              key: "push_notifications",
              label: "Notificações push",
              description: "Receba notificações em tempo real",
            },
            {
              key: "friend_request_notifications",
              label: "Solicitações de amizade",
              description: "Quando alguém te envia uma solicitação",
            },
            {
              key: "comment_notifications",
              label: "Comentários",
              description: "Quando alguém comenta em seus posts",
            },
          ].map(({ key, label, description }) => (
            <div key={key} className="flex items-center justify-between">
              <div>
                <div className="text-gray-700 font-medium">{label}</div>
                <div className="text-sm text-gray-500">{description}</div>
              </div>
              <input
                type="checkbox"
                checked={
                  notificationSettings[key as keyof typeof notificationSettings]
                }
                onChange={(e) =>
                  setNotificationSettings((prev) => ({
                    ...prev,
                    [key]: e.target.checked,
                  }))
                }
                className="w-5 h-5 text-blue-600 rounded focus:ring-blue-500"
              />
            </div>
          ))}
        </div>
      </div>

      <div className="flex justify-end">
        <button
          onClick={handleSaveNotifications}
          disabled={loading}
          className="flex items-center space-x-2 bg-blue-600 hover:bg-blue-700 disabled:bg-blue-400 text-white px-6 py-3 rounded-xl font-medium transition-colors"
        >
          {saved ? <Check className="w-5 h-5" /> : <Save className="w-5 h-5" />}
          <span>
            {saved ? "Salvo!" : loading ? "Salvando..." : "Salvar Alterações"}
          </span>
        </button>
      </div>
    </div>
  );

  const renderAccountSection = () => (
    <div className="space-y-8">
      <div>
        <h2 className="text-2xl font-bold text-gray-900 mb-2">
          Gerenciar Conta
        </h2>
        <p className="text-gray-600">Configurações avançadas da sua conta</p>
      </div>

      <div className="bg-white p-6 rounded-xl shadow-sm border">
        <h3 className="text-lg font-semibold text-gray-900 mb-4">Segurança</h3>
        <div className="space-y-4">
          <div className="flex items-center justify-between">
            <div>
              <div className="text-gray-700 font-medium">Alterar senha</div>
              <div className="text-sm text-gray-500">
                Última alteração há 3 meses
              </div>
            </div>
            <button className="text-blue-600 hover:text-blue-700 font-medium">
              Alterar
            </button>
          </div>
        </div>
      </div>

      <div className="bg-red-50 p-6 rounded-xl border border-red-200">
        <h3 className="text-lg font-semibold text-red-900 mb-4">
          Zona de Perigo
        </h3>
        <div className="space-y-4">
          <div className="flex items-center justify-between">
            <div>
              <div className="text-red-700 font-medium">Desativar conta</div>
              <div className="text-sm text-red-600">
                Oculte temporariamente sua conta
              </div>
            </div>
            <button className="text-red-600 hover:text-red-700 font-medium">
              Desativar
            </button>
          </div>
          <div className="flex items-center justify-between">
            <div>
              <div className="text-red-700 font-medium">Excluir conta</div>
              <div className="text-sm text-red-600">
                Exclua permanentemente sua conta e dados
              </div>
            </div>
            <button className="text-red-600 hover:text-red-700 font-medium">
              Excluir
            </button>
          </div>
        </div>
      </div>
    </div>
  );

  return (
    <div className="min-h-screen bg-gray-50">
      <div className="max-w-6xl mx-auto px-4 py-8">
        {/* Header */}
        <div className="flex items-center space-x-4 mb-8">
          <button
            onClick={() => navigate("/")}
            className="p-2 hover:bg-gray-100 rounded-full transition-colors"
          >
            <ArrowLeft className="w-6 h-6 text-gray-600" />
          </button>
          <h1 className="text-3xl font-bold text-gray-900">Configurações</h1>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-4 gap-8">
          {/* Sidebar */}
          <div className="lg:col-span-1">
            <div className="bg-white rounded-xl shadow-sm border p-2 space-y-1">
              {sections.map((section) => {
                const Icon = section.icon;
                return (
                  <button
                    key={section.id}
                    onClick={() => setActiveSection(section.id)}
                    className={`w-full flex items-center space-x-3 px-4 py-3 text-left rounded-xl transition-colors ${
                      activeSection === section.id
                        ? "bg-blue-100 text-blue-700 border border-blue-200"
                        : "text-gray-700 hover:bg-gray-100"
                    }`}
                  >
                    <Icon className="w-5 h-5" />
                    <span className="font-medium">{section.label}</span>
                  </button>
                );
              })}
            </div>
          </div>

          {/* Content */}
          <div className="lg:col-span-3">
            {activeSection === "profile" && renderProfileSection()}
            {activeSection === "privacy" && renderPrivacySection()}
            {activeSection === "notifications" && renderNotificationsSection()}
            {activeSection === "account" && renderAccountSection()}
            {activeSection === "appearance" && (
              <div className="text-center py-12">
                <Palette className="w-12 h-12 text-gray-400 mx-auto mb-4" />
                <h3 className="text-lg font-medium text-gray-900 mb-2">
                  Em breve
                </h3>
                <p className="text-gray-600">
                  Configurações de aparência estarão disponíveis em breve
                </p>
              </div>
            )}
            {activeSection === "language" && (
              <div className="text-center py-12">
                <Globe className="w-12 h-12 text-gray-400 mx-auto mb-4" />
                <h3 className="text-lg font-medium text-gray-900 mb-2">
                  Em breve
                </h3>
                <p className="text-gray-600">
                  Configurações de idioma estarão disponíveis em breve
                </p>
              </div>
            )}
            {activeSection === "data" && (
              <div className="text-center py-12">
                <Download className="w-12 h-12 text-gray-400 mx-auto mb-4" />
                <h3 className="text-lg font-medium text-gray-900 mb-2">
                  Em breve
                </h3>
                <p className="text-gray-600">
                  Gerenciamento de dados estará disponível em breve
                </p>
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}
