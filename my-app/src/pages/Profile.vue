<script setup>
import { ref, onMounted } from "vue";
import { useRouter } from "vue-router";
import Navbar from "../components/Navbar.vue";
import Footer from "../components/Footer.vue";

const router = useRouter();
const user = ref(null);
const isEditing = ref(false);
const isLoading = ref(true);
const editForm = ref({
  username: ""
});

const getAuthHeader = () => {
    const storedUser = localStorage.getItem("user");
    if (storedUser) {
        const parsed = JSON.parse(storedUser);
        if (parsed.token) return `Bearer ${parsed.token}`;
    }
    return null;
};

const fetchProfile = async () => {
    const token = getAuthHeader();
    if (!token) {
        handleLogout();
        return;
    }

    try {
        const res = await fetch(`${import.meta.env.VITE_API_BASE_URL}/api/profile`, {
            headers: { 'Authorization': token }
        });
        
        if (res.ok) {
            const data = await res.json();
            user.value = data;
            
            // Update local storage to keep in sync (optional but good for consistency)
            const stored = JSON.parse(localStorage.getItem("user") || '{}');
            stored.username = data.username;
            stored.plan = data.plan;
            localStorage.setItem("user", JSON.stringify(stored));
            
            editForm.value.username = data.username;
        } else {
            if (res.status === 401) handleLogout();
            else console.error("Failed to fetch profile");
        }
    } catch (e) {
        console.error("Error fetching profile:", e);
    } finally {
        isLoading.value = false;
    }
};

onMounted(() => {
  fetchProfile();
});

const toggleEdit = () => {
  isEditing.value = !isEditing.value;
  if (isEditing.value && user.value) {
    editForm.value.username = user.value.username;
  }
};

const saveProfile = async () => {
  if (!editForm.value.username.trim()) {
    alert("Username tidak boleh kosong");
    return;
  }

  const token = getAuthHeader();
  if (!token) return;

  try {
      const res = await fetch(`${import.meta.env.VITE_API_BASE_URL}/api/profile`, {
          method: 'PUT',
          headers: { 
              'Content-Type': 'application/json',
              'Authorization': token 
          },
          body: JSON.stringify({ username: editForm.value.username })
      });
      
      const data = await res.json();
      
      if (res.ok) {
          alert(data.message || "Profil berhasil diperbarui!");
          
          if (data.username !== user.value.username) {
               // Username changed, force logout for security/token refresh
               alert("Username berubah. Silakan login kembali.");
               handleLogout();
          } else {
               // Just update local view
               user.value.username = data.username;
               isEditing.value = false;
               
               // Update local storage
               const stored = JSON.parse(localStorage.getItem("user") || '{}');
               stored.username = data.username;
               localStorage.setItem("user", JSON.stringify(stored));
          }
      } else {
          alert(data.error || "Gagal memperbarui profil");
      }
  } catch (e) {
      alert("Terjadi kesalahan koneksi.");
      console.error(e);
  }
};

const handleLogout = () => {
  localStorage.removeItem("user");
  router.push("/");
  window.location.href = "/"; 
};
</script>

<template>
  <div class="min-h-screen bg-[#050716] text-white font-sans selection:bg-[#6C4DFF] selection:text-white flex flex-col">
    <Navbar />

    <main class="flex-grow pt-32 pb-20 px-4">
      <div class="max-w-4xl mx-auto">
        <h1 class="text-3xl font-bold mb-8">Profil Saya</h1>

        <div v-if="isLoading" class="flex justify-center py-20">
            <div class="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-[#6C4DFF]"></div>
        </div>

        <div v-else-if="user" class="bg-[#0B0F1A] border border-gray-800 rounded-2xl p-8 shadow-xl flex flex-col md:flex-row gap-8 items-start">
          
          <!-- Avatar Section -->
          <div class="flex-shrink-0">
            <div class="w-32 h-32 bg-[#1A1625] rounded-full flex items-center justify-center border-2 border-[#6C4DFF]">
              <span class="text-5xl font-bold text-[#6C4DFF]">{{ user.username ? user.username.charAt(0).toUpperCase() : '?' }}</span>
            </div>
          </div>

          <!-- User Info Section -->
          <div class="flex-grow space-y-6">
            <div>
              <label class="block text-sm text-gray-500 mb-1">Username</label>
              <div v-if="!isEditing" class="text-xl font-semibold">{{ user.username }}</div>
              <input 
                v-else
                v-model="editForm.username"
                type="text"
                class="bg-[#151926] border border-gray-700 rounded px-3 py-1 text-white focus:outline-none focus:border-[#6C4DFF]"
              />
            </div>

            <div>
              <label class="block text-sm text-gray-500 mb-1">Paket Saat Ini</label>
              <div class="inline-flex items-center px-3 py-1 rounded-full bg-[#6C4DFF]/10 text-[#6C4DFF] border border-[#6C4DFF]/20 text-sm font-medium">
                {{ user.plan ? user.plan.toUpperCase() : 'FREE' }}
              </div>
            </div>

            <div>
              <label class="block text-sm text-gray-500 mb-1">Status Akun</label>
              <div class="text-green-400 flex items-center gap-2">
                <span class="w-2 h-2 rounded-full bg-green-400"></span>
                Aktif
              </div>
            </div>
          </div>

          <!-- Actions -->
          <div class="flex flex-col gap-3 w-full md:w-auto">
            <button 
              v-if="!isEditing"
              @click="toggleEdit"
              class="px-6 py-2 border border-gray-600 hover:border-gray-400 rounded-lg transition-colors text-sm"
            >
              Edit Profil
            </button>
            <div v-else class="flex flex-col gap-2">
                <button 
                  @click="saveProfile"
                  class="px-6 py-2 bg-[#6C4DFF] hover:bg-[#5839EE] text-white rounded-lg transition-colors text-sm"
                >
                  Simpan
                </button>
                <button 
                  @click="toggleEdit"
                  class="px-6 py-2 border border-gray-600 hover:border-gray-400 rounded-lg transition-colors text-sm"
                >
                  Batal
                </button>
            </div>
            <button @click="handleLogout" class="px-6 py-2 bg-red-500/10 text-red-500 hover:bg-red-500/20 rounded-lg transition-colors text-sm border border-red-500/20">
              Keluar
            </button>
          </div>

        </div>
        
        <div v-else class="text-center py-10 flex flex-col items-center gap-4">
            <p class="text-gray-400">Gagal memuat profil.</p>
            <div class="flex gap-4">
                <button @click="fetchProfile" class="text-[#6C4DFF] hover:underline">Coba lagi</button>
                <span class="text-gray-600">|</span>
                <button @click="handleLogout" class="text-red-500 hover:text-red-400 hover:underline">Keluar</button>
            </div>
        </div>

        <!-- Recent Activity Placeholder -->
        <div class="mt-12">
            <h2 class="text-xl font-bold mb-4">Aktivitas Terakhir</h2>
            <div class="bg-[#0B0F1A] border border-gray-800 rounded-2xl p-8 text-gray-500 text-center">
                Belum ada aktivitas tercatat.
            </div>
        </div>

      </div>
    </main>

    <Footer />
  </div>
</template>
