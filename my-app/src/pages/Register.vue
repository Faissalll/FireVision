<script setup>
import { ref } from "vue";
import { useRouter } from "vue-router";
import Navbar from "../components/Navbar.vue";
import Footer from "../components/Footer.vue";

const router = useRouter();
const username = ref("");
const password = ref("");
const confirmPassword = ref("");
const errorMessage = ref("");
const successMessage = ref("");
const isLoading = ref(false);

const handleRegister = async () => {
    isLoading.value = true;
    errorMessage.value = "";
    successMessage.value = "";

    if (password.value !== confirmPassword.value) {
        errorMessage.value = "Password tidak cocok";
        isLoading.value = false;
        return;
    }

    try {
        const response = await fetch("http://localhost:5001/api/register", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
                username: username.value,
                password: password.value,
            }),
        });

        const data = await response.json();

        if (response.ok) {
            successMessage.value = "Registrasi berhasil! Mengalihkan ke login...";
            setTimeout(() => {
                router.push("/login");
            }, 1500);
        } else {
            errorMessage.value = data.error || "Registrasi gagal";
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
                <h2 class="text-3xl font-bold text-center mb-2 text-white">Buat Akun</h2>
                <p class="text-gray-400 text-center mb-8">Daftar untuk mulai menggunakan FireVision</p>

                <form @submit.prevent="handleRegister" class="space-y-6">

                    <!-- Username -->
                    <div>
                        <label class="block text-gray-400 text-sm font-medium mb-2">Username</label>
                        <input v-model="username" type="text" required
                            class="w-full bg-[#151926] border border-gray-700 rounded-lg px-4 py-3 text-white focus:outline-none focus:border-[#6C4DFF] focus:ring-1 focus:ring-[#6C4DFF] transition-all"
                            placeholder="Pilih username" />
                    </div>

                    <!-- Password -->
                    <div>
                        <label class="block text-gray-400 text-sm font-medium mb-2">Password</label>
                        <input v-model="password" type="password" required
                            class="w-full bg-[#151926] border border-gray-700 rounded-lg px-4 py-3 text-white focus:outline-none focus:border-[#6C4DFF] focus:ring-1 focus:ring-[#6C4DFF] transition-all"
                            placeholder="••••••••" />
                    </div>

                    <!-- Confirm Password -->
                    <div>
                        <label class="block text-gray-400 text-sm font-medium mb-2">Konfirmasi Password</label>
                        <input v-model="confirmPassword" type="password" required
                            class="w-full bg-[#151926] border border-gray-700 rounded-lg px-4 py-3 text-white focus:outline-none focus:border-[#6C4DFF] focus:ring-1 focus:ring-[#6C4DFF] transition-all"
                            placeholder="••••••••" />
                    </div>

                    <!-- Messages -->
                    <div v-if="errorMessage" class="text-red-500 text-sm text-center">
                        {{ errorMessage }}
                    </div>
                    <div v-if="successMessage" class="text-green-500 text-sm text-center">
                        {{ successMessage }}
                    </div>

                    <!-- Register Button -->
                    <button type="submit" :disabled="isLoading"
                        class="w-full bg-[#6C4DFF] hover:bg-[#5839EE] text-white font-bold py-3 rounded-lg transition-all duration-300 transform hover:-translate-y-1 shadow-lg shadow-[#6C4DFF]/30 disabled:opacity-50 disabled:cursor-not-allowed">
                        <span v-if="isLoading">Loading...</span>
                        <span v-else>Daftar</span>
                    </button>
                </form>

                <p class="text-gray-400 text-center mt-6 text-sm">
                    Sudah punya akun?
                    <router-link to="/login"
                        class="text-[#6C4DFF] hover:text-[#886CFF] font-semibold transition-colors">
                        Masuk disini
                    </router-link>
                </p>
            </div>
        </main>

        <Footer />
    </div>
</template>
