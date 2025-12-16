<script setup>
import { ref } from "vue";
import { useRouter } from "vue-router";
import Navbar from "../components/Navbar.vue";
import Footer from "../components/Footer.vue";
import { auth } from "../store/auth";

const router = useRouter();
const username = ref("");
const password = ref("");
const errorMessage = ref("");
const isLoading = ref(false);

const handleLogin = async () => {
  isLoading.value = true;
  errorMessage.value = "";

  try {
    const response = await fetch(`${import.meta.env.VITE_API_BASE_URL}/api/login`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        username: username.value,
        password: password.value,
      }),
    });

    const data = await response.json();

    if (response.ok) {
      // Store user session via reactive store
      auth.login({ 
        username: data.username,
        plan: data.plan,
        token: data.token
      });
      router.push("/demo"); 
    } else {
      errorMessage.value = data.error || "Login gagal";
    }
  } catch (error) {
    errorMessage.value = "Terjadi kesalahan koneksi";
    console.error(error);
  } finally {
    isLoading.value = false;
  }
};
</script>

<template>
  <div class="min-h-screen bg-[#050716] text-white font-sans selection:bg-[#6C4DFF] selection:text-white flex flex-col">
    <Navbar />

    <main class="flex-grow flex items-center justify-center pt-20 pb-20 px-4">
      <div class="bg-[#0B0F1A] border border-gray-800 rounded-2xl p-8 w-full max-w-md shadow-2xl">
        <h2 class="text-3xl font-bold text-center mb-2 text-white">Selamat Datang</h2>
        <p class="text-gray-400 text-center mb-8">Masuk untuk melanjutkan ke FireVision</p>

        <form @submit.prevent="handleLogin" class="space-y-6">
          
          <!-- Username -->
          <div>
            <label class="block text-gray-400 text-sm font-medium mb-2">Username</label>
            <input 
              v-model="username" 
              type="text" 
              required
              class="w-full bg-[#151926] border border-gray-700 rounded-lg px-4 py-3 text-white focus:outline-none focus:border-[#6C4DFF] focus:ring-1 focus:ring-[#6C4DFF] transition-all"
              placeholder="Masukkan username Anda"
            />
          </div>

          <!-- Password -->
          <div>
            <label class="block text-gray-400 text-sm font-medium mb-2">Password</label>
            <input 
              v-model="password" 
              type="password" 
              required
              class="w-full bg-[#151926] border border-gray-700 rounded-lg px-4 py-3 text-white focus:outline-none focus:border-[#6C4DFF] focus:ring-1 focus:ring-[#6C4DFF] transition-all"
              placeholder="••••••••"
            />
          </div>

          <div class="flex justify-end">
             <router-link to="/forgot-password" class="text-sm text-[#6C4DFF] hover:underline">Lupa Password?</router-link>
          </div>

          <!-- Error Message -->
          <div v-if="errorMessage" class="text-red-500 text-sm text-center">
            {{ errorMessage }}
          </div>

          <!-- Login Button -->
          <button 
            type="submit" 
            :disabled="isLoading"
            class="w-full bg-[#6C4DFF] hover:bg-[#5839EE] text-white font-bold py-3 rounded-lg transition-all duration-300 transform hover:-translate-y-1 shadow-lg shadow-[#6C4DFF]/30 disabled:opacity-50 disabled:cursor-not-allowed"
          >
            <span v-if="isLoading">Loading...</span>
            <span v-else>Masuk</span>
          </button>
        </form>

        <p class="text-gray-400 text-center mt-6 text-sm">
          Belum punya akun? 
          <router-link to="/register" class="text-[#6C4DFF] hover:text-[#886CFF] font-semibold transition-colors">
            Daftar sekarang
          </router-link>
        </p>
      </div>
    </main>

    <Footer />
  </div>
</template>
