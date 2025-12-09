<script setup>
import { ref, onMounted } from "vue";
import { useRouter } from "vue-router";
import Navbar from "../components/Navbar.vue";
import Footer from "../components/Footer.vue";

const router = useRouter();
const user = ref(null);

onMounted(() => {
  const storedUser = localStorage.getItem("user");
  if (storedUser) {
    user.value = JSON.parse(storedUser);
  } else {
    router.push("/login"); // Redirect if not logged in
  }
});

const handleLogout = () => {
  localStorage.removeItem("user");
  router.push("/");
  // Refresh page to update Navbar state implies a reload or we can use an event bus/pinia. 
  // For simplicity doing a full reload or letting Navbar handle it via router check if we had global state.
  // Ideally Navbar reacts to localStorage changes or we use a reactive state management.
  // For now simple router push, Navbar needs to know. 
  // We'll address Navbar reactivity in the Navbar component update.
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
              <div class="text-xl font-semibold">{{ user.username }}</div>
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
            <button class="px-6 py-2 border border-gray-600 hover:border-gray-400 rounded-lg transition-colors text-sm">
              Edit Profil
            </button>
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
