<script setup>
import { ref, onMounted } from "vue";
import { useRouter, useRoute } from "vue-router";
import Navbar from "../components/Navbar.vue";
import Footer from "../components/Footer.vue";

const route = useRoute();
const router = useRouter();

const token = ref("");
const password = ref("");
const confirmPassword = ref("");
const message = ref("");
const errorMessage = ref("");
const isLoading = ref(false);

onMounted(() => {
    token.value = route.query.token || "";
    if (!token.value) {
        errorMessage.value = "Token tidak valid atau hilang.";
    }
});

const handleReset = async () => {
    isLoading.value = true;
    errorMessage.value = "";
    message.value = "";

    if (password.value !== confirmPassword.value) {
        errorMessage.value = "Password tidak cocok.";
        isLoading.value = false;
        return;
    }

    try {
        const res = await fetch(`${import.meta.env.VITE_API_BASE_URL}/api/reset-password`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ token: token.value, password: password.value })
        });
        const data = await res.json();
        
        if (res.ok) {
            message.value = "Password berhasil direset! Mengalihkan ke login...";
            setTimeout(() => {
                router.push("/login");
            }, 2000);
        } else {
            errorMessage.value = data.error || "Gagal mereset password.";
        }
    } catch (e) {
        errorMessage.value = "Kesalahan koneksi.";
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
                <h2 class="text-3xl font-bold text-center mb-2 text-white">Reset Password</h2>
                <p class="text-gray-400 text-center mb-8">Masukkan password baru Anda</p>

                <form @submit.prevent="handleReset" class="space-y-6">
                    <div>
                        <label class="block text-gray-400 text-sm font-medium mb-2">Password Baru</label>
                        <input v-model="password" type="password" required
                            class="w-full bg-[#151926] border border-gray-700 rounded-lg px-4 py-3 text-white focus:outline-none focus:border-[#6C4DFF] focus:ring-1 focus:ring-[#6C4DFF] transition-all"
                            placeholder="••••••••" />
                    </div>
                    <div>
                        <label class="block text-gray-400 text-sm font-medium mb-2">Konfirmasi Password</label>
                        <input v-model="confirmPassword" type="password" required
                            class="w-full bg-[#151926] border border-gray-700 rounded-lg px-4 py-3 text-white focus:outline-none focus:border-[#6C4DFF] focus:ring-1 focus:ring-[#6C4DFF] transition-all"
                            placeholder="••••••••" />
                    </div>

                    <div v-if="message" class="text-green-400 text-sm text-center bg-green-500/10 p-3 rounded border border-green-500/20">
                        {{ message }}
                    </div>
                    <div v-if="errorMessage" class="text-red-500 text-sm text-center">
                        {{ errorMessage }}
                    </div>

                    <button type="submit" :disabled="isLoading || !token"
                        class="w-full bg-[#6C4DFF] hover:bg-[#5839EE] text-white font-bold py-3 rounded-lg transition-all duration-300 transform hover:-translate-y-1 shadow-lg shadow-[#6C4DFF]/30 disabled:opacity-50 disabled:cursor-not-allowed">
                        <span v-if="isLoading">Processing...</span>
                        <span v-else>Reset Password</span>
                    </button>
                </form>
            </div>
        </main>
        <Footer />
    </div>
</template>
