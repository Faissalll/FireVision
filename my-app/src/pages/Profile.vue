<script setup>
import { ref, onMounted } from "vue";
import { useRouter } from "vue-router";
import Navbar from "../components/Navbar.vue";
import Footer from "../components/Footer.vue";

const router = useRouter();
const user = ref(null);
const isEditing = ref(false);
const editForm = ref({
  username: ""
});

onMounted(() => {
  const storedUser = localStorage.getItem("user");
  if (storedUser) {
    user.value = JSON.parse(storedUser);
    editForm.value.username = user.value.username;
  } else {
    router.push("/login"); // Redirect if not logged in
  }
});

const toggleEdit = () => {
  isEditing.value = !isEditing.value;
  if (isEditing.value) {
    editForm.value.username = user.value.username;
  }
};

const saveProfile = () => {
  if (!editForm.value.username.trim()) {
    alert("Username tidak boleh kosong");
    return;
  }

  // Update local object
  user.value.username = editForm.value.username;
  
  // Update localStorage
  localStorage.setItem("user", JSON.stringify(user.value));
  
  // Exit edit mode
  isEditing.value = false;
  alert("Profil berhasil diperbarui!");
  
  // Optional: Force reload to update Navbar if not using reactive store globally yet
  // window.location.reload(); 
  // Better: emits or simple alert is enough for now as requested "Mock/Simple"
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

        <div v-if="user" class="bg-[#0B0F1A] border border-gray-800 rounded-2xl p-8 shadow-xl flex flex-col md:flex-row gap-8 items-start">
          
          <!-- Avatar Section -->
          <div class="flex-shrink-0">
            <div class="w-32 h-32 bg-[#1A1625] rounded-full flex items-center justify-center border-2 border-[#6C4DFF]">
              <span class="text-5xl font-bold text-[#6C4DFF]">{{ user.username.charAt(0).toUpperCase() }}</span>
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
                Starter (Free Trial)
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
