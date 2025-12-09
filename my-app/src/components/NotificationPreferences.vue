<script setup>
import { ref } from 'vue';

// Mock State for Telegram
const telegramConfig = ref({
    enabled: false,
    botToken: '',
    chatId: ''
});

// Mock State for Email
const emailConfig = ref({
    enabled: false,
    smtpHost: '',
    smtpPort: '587',
    senderEmail: '',
    password: '',
    recipientEmail: ''
});

// Mock State for Sound & Browser
const alertConfig = ref({
    browserPopup: true,
    soundEnabled: true,
    volume: 80,
    soundType: 'Siren 1'
});

// Feedback State
const telegramStatus = ref(null); // 'success', 'error', or null
const emailStatus = ref(null);

const testTelegram = () => {
    // Simulate API call
    telegramStatus.value = null;
    if(!telegramConfig.value.botToken || !telegramConfig.value.chatId) {
        telegramStatus.value = 'error';
        return;
    }
    setTimeout(() => {
        telegramStatus.value = 'success';
    }, 1000);
};

const testEmail = () => {
    emailStatus.value = null;
    if(!emailConfig.value.recipientEmail) {
        emailStatus.value = 'error';
        return;
    }
    setTimeout(() => {
        emailStatus.value = 'success';
    }, 1500);
};
</script>

<template>
    <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        
        <!-- 1. Telegram Card -->
        <div class="bg-[#0B0F1A] rounded-2xl p-6 border border-gray-800/50 shadow-lg hover:border-[#6C4DFF]/30 transition-all animate-fade-in-up" style="animation-delay: 0.1s;">
            <div class="flex items-center gap-3 mb-6">
                <div class="w-10 h-10 rounded-full bg-[#2AABEE]/10 flex items-center justify-center text-[#2AABEE]">
                    <svg xmlns="http://www.w3.org/2000/svg" width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="m22 2-7 20-4-9-9-4Z"/><path d="M22 2 11 13"/></svg>
                </div>
                <h2 class="text-xl font-bold text-white">Telegram</h2>
            </div>

            <p class="text-gray-400 text-sm mb-6 min-h-[40px]">
                Kirim peringatan otomatis ke grup atau akun Telegram Anda secara real-time.
            </p>

            <div class="space-y-4">
                <div>
                    <label class="block text-xs font-semibold text-gray-500 uppercase tracking-wider mb-1">Bot Token</label>
                    <input v-model="telegramConfig.botToken" type="text" class="w-full bg-[#151926] border border-gray-700 rounded-lg px-4 py-2.5 text-sm focus:outline-none focus:border-[#2AABEE] transition-colors" placeholder="123456:ABC-DEF1234ghIkl-zyx57W2v1u123ew11" />
                </div>
                <div>
                    <label class="block text-xs font-semibold text-gray-500 uppercase tracking-wider mb-1">Chat ID</label>
                    <input v-model="telegramConfig.chatId" type="text" class="w-full bg-[#151926] border border-gray-700 rounded-lg px-4 py-2.5 text-sm focus:outline-none focus:border-[#2AABEE] transition-colors" placeholder="-100123456789" />
                </div>

                <div class="flex items-center justify-between py-2">
                    <span class="text-sm font-medium text-gray-300">Aktifkan Notifikasi</span>
                    <label class="relative inline-flex items-center cursor-pointer">
                        <input type="checkbox" v-model="telegramConfig.enabled" class="sr-only peer">
                        <div class="w-11 h-6 bg-gray-700 peer-focus:outline-none rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:border-gray-300 after:border after:rounded-full after:h-5 after:w-5 after:transition-all peer-checked:bg-[#2AABEE]"></div>
                    </label>
                </div>

                <div class="pt-4 border-t border-gray-800">
                    <button @click="testTelegram" class="w-full py-2 bg-[#2AABEE]/10 hover:bg-[#2AABEE]/20 text-[#2AABEE] rounded-lg text-sm font-semibold transition-colors flex items-center justify-center gap-2">
                        <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="m22 2-7 20-4-9-9-4Z"/><path d="M22 2 11 13"/></svg>
                        Kirim Pesan Uji Coba
                    </button>
                    
                    <p v-if="telegramStatus === 'success'" class="text-green-500 text-xs mt-2 text-center">✓ Pesan terkirim! Cek Telegram Anda.</p>
                    <p v-if="telegramStatus === 'error'" class="text-red-500 text-xs mt-2 text-center">⚠ Gagal. Cek Token dan Chat ID.</p>
                </div>
            </div>
        </div>

        <!-- 2. Email Card -->
        <div class="bg-[#0B0F1A] rounded-2xl p-6 border border-gray-800/50 shadow-lg hover:border-[#6C4DFF]/30 transition-all animate-fade-in-up" style="animation-delay: 0.2s;">
            <div class="flex items-center gap-3 mb-6">
                <div class="w-10 h-10 rounded-full bg-[#ea4335]/10 flex items-center justify-center text-[#ea4335]">
                    <svg xmlns="http://www.w3.org/2000/svg" width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect width="20" height="16" x="2" y="4" rx="2"/><path d="m22 7-8.97 5.7a1.94 1.94 0 0 1-2.06 0L2 7"/></svg>
                </div>
                <h2 class="text-xl font-bold text-white">Email</h2>
            </div>

            <p class="text-gray-400 text-sm mb-6 min-h-[40px]">
                Gunakan email untuk laporan deteksi detail dan peringatan darurat.
            </p>

            <div class="space-y-4">
                <div class="grid grid-cols-3 gap-2">
                    <div class="col-span-2">
                        <label class="block text-xs font-semibold text-gray-500 uppercase tracking-wider mb-1">SMTP Host</label>
                        <input v-model="emailConfig.smtpHost" type="text" class="w-full bg-[#151926] border border-gray-700 rounded-lg px-4 py-2.5 text-sm focus:outline-none focus:border-[#ea4335]" placeholder="smtp.gmail.com" />
                    </div>
                    <div>
                        <label class="block text-xs font-semibold text-gray-500 uppercase tracking-wider mb-1">Port</label>
                        <input v-model="emailConfig.smtpPort" type="text" class="w-full bg-[#151926] border border-gray-700 rounded-lg px-4 py-2.5 text-sm focus:outline-none focus:border-[#ea4335]" placeholder="587" />
                    </div>
                </div>

                <div>
                    <label class="block text-xs font-semibold text-gray-500 uppercase tracking-wider mb-1">Email Pengirim</label>
                    <input v-model="emailConfig.senderEmail" type="email" class="w-full bg-[#151926] border border-gray-700 rounded-lg px-4 py-2.5 text-sm focus:outline-none focus:border-[#ea4335]" placeholder="alert@firevision.id" />
                </div>
                 <div>
                    <label class="block text-xs font-semibold text-gray-500 uppercase tracking-wider mb-1">Password App</label>
                    <input v-model="emailConfig.password" type="password" class="w-full bg-[#151926] border border-gray-700 rounded-lg px-4 py-2.5 text-sm focus:outline-none focus:border-[#ea4335]" placeholder="••••••••" />
                </div>
                <div>
                    <label class="block text-xs font-semibold text-gray-500 uppercase tracking-wider mb-1">Email Tujuan</label>
                    <input v-model="emailConfig.recipientEmail" type="email" class="w-full bg-[#151926] border border-gray-700 rounded-lg px-4 py-2.5 text-sm focus:outline-none focus:border-[#ea4335]" placeholder="admin@perusahaan.com" />
                </div>

                 <div class="flex items-center justify-between py-2">
                    <span class="text-sm font-medium text-gray-300">Aktifkan Email</span>
                    <label class="relative inline-flex items-center cursor-pointer">
                        <input type="checkbox" v-model="emailConfig.enabled" class="sr-only peer">
                        <div class="w-11 h-6 bg-gray-700 peer-focus:outline-none rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:border-gray-300 after:border after:rounded-full after:h-5 after:w-5 after:transition-all peer-checked:bg-[#ea4335]"></div>
                    </label>
                </div>

                <div class="pt-4 border-t border-gray-800">
                     <button @click="testEmail" class="w-full py-2 bg-[#ea4335]/10 hover:bg-[#ea4335]/20 text-[#ea4335] rounded-lg text-sm font-semibold transition-colors flex items-center justify-center gap-2">
                        <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect width="20" height="16" x="2" y="4" rx="2"/><path d="m22 7-8.97 5.7a1.94 1.94 0 0 1-2.06 0L2 7"/></svg>
                        Kirim Email Uji Coba
                    </button>
                    <p v-if="emailStatus === 'success'" class="text-green-500 text-xs mt-2 text-center">✓ Email terkirim! Cek inbox Anda.</p>
                    <p v-if="emailStatus === 'error'" class="text-red-500 text-xs mt-2 text-center">⚠ Gagal. Cek konfigurasi SMTP/Email.</p>
                </div>
            </div>
        </div>

        <!-- 3. Sound & Browser -->
        <div class="bg-[#0B0F1A] rounded-2xl p-6 border border-gray-800/50 shadow-lg hover:border-[#6C4DFF]/30 transition-all animate-fade-in-up" style="animation-delay: 0.3s;">
            <div class="flex items-center gap-3 mb-6">
                <div class="w-10 h-10 rounded-full bg-[#6C4DFF]/10 flex items-center justify-center text-[#6C4DFF]">
                    <svg xmlns="http://www.w3.org/2000/svg" width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M6 9H4.5a2.5 2.5 0 0 1 0-5H6"/><path d="M18 9h1.5a2.5 2.5 0 0 0 0-5H18"/><path d="M4 22h16"/><path d="M10 14.66V17c0 .55-.47.98-.97 1.21C7.85 18.75 7 20.24 7 22"/><path d="M14 14.66V17c0 .55.47.98.97 1.21C16.15 18.75 17 20.24 17 22"/><path d="M18 2H6v7a6 6 0 0 0 12 0V2Z"/></svg>
                </div>
                <h2 class="text-xl font-bold text-white">Browser & Suara</h2>
            </div>

            <p class="text-gray-400 text-sm mb-6 min-h-[40px]">
                Pengaturan notifikasi lokal pada browser dan alarm suara saat halaman dibuka.
            </p>

            <div class="space-y-6">
                <!-- Volume Control -->
                <div>
                    <div class="flex justify-between mb-2">
                        <label class="text-xs font-semibold text-gray-500 uppercase">Volume Alarm</label>
                        <span class="text-xs font-mono text-[#6C4DFF]">{{ alertConfig.volume }}%</span>
                    </div>
                    <input type="range" v-model="alertConfig.volume" class="w-full h-2 bg-gray-700 rounded-lg appearance-none cursor-pointer accent-[#6C4DFF]" />
                </div>

                 <!-- Sound Type -->
                <div>
                    <label class="block text-xs font-semibold text-gray-500 uppercase tracking-wider mb-2">Jenis Suara</label>
                    <select v-model="alertConfig.soundType" class="w-full bg-[#151926] border border-gray-700 rounded-lg px-4 py-2.5 text-sm focus:outline-none focus:border-[#6C4DFF]">
                        <option>Siren 1 (Standard)</option>
                        <option>Siren 2 (Urgent)</option>
                        <option>Beep (Subtle)</option>
                    </select>
                </div>

                <!-- Toggles -->
                <div class="space-y-4 pt-2">
                     <div class="flex items-center justify-between">
                        <div class="flex flex-col">
                            <span class="text-sm font-medium text-gray-300">Notifikasi Popup</span>
                            <span class="text-xs text-gray-500">Tampilkan popup browser saat terminimize</span>
                        </div>
                        <label class="relative inline-flex items-center cursor-pointer">
                            <input type="checkbox" v-model="alertConfig.browserPopup" class="sr-only peer">
                            <div class="w-11 h-6 bg-gray-700 peer-focus:outline-none rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:border-gray-300 after:border after:rounded-full after:h-5 after:w-5 after:transition-all peer-checked:bg-[#6C4DFF]"></div>
                        </label>
                    </div>
                     <div class="flex items-center justify-between">
                        <div class="flex flex-col">
                            <span class="text-sm font-medium text-gray-300">Suara Alarm</span>
                            <span class="text-xs text-gray-500">Mainkan suara saat api terdeteksi</span>
                        </div>
                        <label class="relative inline-flex items-center cursor-pointer">
                            <input type="checkbox" v-model="alertConfig.soundEnabled" class="sr-only peer">
                            <div class="w-11 h-6 bg-gray-700 peer-focus:outline-none rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:border-gray-300 after:border after:rounded-full after:h-5 after:w-5 after:transition-all peer-checked:bg-[#6C4DFF]"></div>
                        </label>
                    </div>
                </div>

                 <div class="pt-4 border-t border-gray-800">
                     <button class="w-full py-2 bg-gray-800 hover:bg-gray-700 text-white rounded-lg text-sm font-semibold transition-colors">
                        Simpan Pengaturan Lokal
                    </button>
                </div>

            </div>
        </div>

    </div>
</template>

<style scoped>
@keyframes fadeInUp {
    from {
        opacity: 0;
        transform: translateY(20px);
    }
    to {
        opacity: 1;
        transform: translateY(0);
    }
}

.animate-fade-in-up {
    animation: fadeInUp 0.6s ease-out forwards;
    opacity: 0;
}
</style>
