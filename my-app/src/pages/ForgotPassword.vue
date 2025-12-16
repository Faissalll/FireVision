<script setup>
import { ref } from "vue";
import { useRouter } from "vue-router";
import Navbar from "../components/Navbar.vue";
import Footer from "../components/Footer.vue";

const email = ref("");
const message = ref("");
const errorMessage = ref("");
const isLoading = ref(false);

const handleForgot = async () => {
    isLoading.value = true;
    message.value = "";
    errorMessage.value = "";

    try {
        const res = await fetch(`${import.meta.env.VITE_API_BASE_URL}/api/forgot-password`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ email: email.value })
        });
        const data = await res.json();
        
        if (res.ok) {
            message.value = data.message;
            // For dev/demo only: show mock token if returned
            if (data.mock_token) {
                console.log("Mock Token:", data.mock_token);
                // Redirect user to reset page directly for ease of testing
                // setTimeout(() => {
                //      window.location.href = `/reset-password?token=${data.mock_token}`;
                // }, 3000);
            }
        } else {
            errorMessage.value = data.error || "Gagal mengirim permintaan.";
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
                <h2 class="text-3xl font-bold text-center mb-2 text-white">Lupa Password</h2>
                <p class="text-gray-400 text-center mb-8">Masukkan email untuk reset password</p>

                <form @submit.prevent="handleForgot" class="space-y-6">
                    <div>
                        <label class="block text-gray-400 text-sm font-medium mb-2">Email</label>
                        <input v-model="email" type="email" required
                            class="w-full bg-[#151926] border border-gray-700 rounded-lg px-4 py-3 text-white focus:outline-none focus:border-[#6C4DFF] focus:ring-1 focus:ring-[#6C4DFF] transition-all"
                            placeholder="nama@email.com" />
                    </div>

                    <div v-if="message" class="text-green-400 text-sm text-center bg-green-500/10 p-3 rounded border border-green-500/20">
                        {{ message }}
                    </div>
                    <div v-if="errorMessage" class="text-red-500 text-sm text-center">
                        {{ errorMessage }}
                    </div>

                    <button type="submit" :disabled="isLoading"
                        class="w-full bg-[#6C4DFF] hover:bg-[#5839EE] text-white font-bold py-3 rounded-lg transition-all duration-300 transform hover:-translate-y-1 shadow-lg shadow-[#6C4DFF]/30 disabled:opacity-50 disabled:cursor-not-allowed">
                        <span v-if="isLoading">Sending...</span>
                        <span v-else>Kirim Link Reset</span>
                    </button>
                    
                    <div class="text-center mt-4">
                        <router-link to="/login" class="text-gray-400 hover:text-white text-sm">Kembali ke Login</router-link>
                    </div>
                </form>
            </div>
        </main>
        <Footer />
    </div>
</template>
