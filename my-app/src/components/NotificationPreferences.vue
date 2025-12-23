<script setup>
import { ref, onMounted } from 'vue';
import alarmSound1 from "../assets/alarm.mp3";
import alarmSound2 from "../assets/alarm2.wav";
import alarmSound3 from "../assets/alarm3.wav";
import { auth } from '../store/auth';

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || "http://127.0.0.1:5001";

// Map sound types to audio sources
const soundSources = {
    siren1: alarmSound1,
    siren2: alarmSound2,
    beep: alarmSound3
};

// Audio Object
const alarmAudio = new Audio(alarmSound1);
alarmAudio.loop = true;

// State for Telegram
const telegramConfig = ref({
    enabled: false,
    botToken: '',
    chatId: ''
});

// State for Email
const emailConfig = ref({
    enabled: false,
    smtpHost: 'smtp.gmail.com',
    smtpPort: '587',
    senderEmail: '',
    password: '',
    recipientEmail: ''
});

// State for Sound & Browser (Local Only)
const alertConfig = ref({
    browserPopup: true,
    soundEnabled: true,
    volume: 80,
    soundType: 'siren1'
});

// Feedback State
const telegramStatus = ref(null);
const emailStatus = ref(null);
const isLoading = ref(false);

// Auto-detect State
const showGuide = ref(false);
const checkingId = ref(false);
const idCheckMsg = ref("");
const idCheckSuccess = ref(false);

const checkChatId = async () => {
    if (!telegramConfig.value.botToken) return;
    
    checkingId.value = true;
    idCheckMsg.value = "";
    idCheckSuccess.value = false;
    
    try {
        const response = await fetch(`${API_BASE_URL}/api/telegram/get-chat-id`, {
             method: 'POST',
             headers: { 
                 'Content-Type': 'application/json',
                 'Authorization': `Bearer ${auth.user.token}`
             },
             body: JSON.stringify({ token: telegramConfig.value.botToken })
        });
        const data = await response.json();
        
        if (response.ok && data.chat_id) {
            telegramConfig.value.chatId = data.chat_id;
            idCheckSuccess.value = true;
            idCheckMsg.value = "Chat ID ditemukan!";
        } else {
            idCheckSuccess.value = false;
            idCheckMsg.value = data.error || "Gagal. Pastikan sudah chat bot Anda.";
        }
    } catch (e) {
        idCheckSuccess.value = false;
        idCheckMsg.value = "Koneksi error.";
    } finally {
        checkingId.value = false;
    }
};

onMounted(async () => {
    // 1. Load Local Sound Settings
    const vol = localStorage.getItem('fv_volume');
    if (vol) alertConfig.value.volume = Number(vol);
    if(alarmAudio) alarmAudio.volume = alertConfig.value.volume / 100;
    
    const popup = localStorage.getItem('fv_popup');
    if (popup) alertConfig.value.browserPopup = (popup === 'true');
    
    const snd = localStorage.getItem('fv_sound');
    if (snd) alertConfig.value.soundEnabled = (snd === 'true');

    const sType = localStorage.getItem('fv_soundType');
    if (sType) alertConfig.value.soundType = sType;

    // 2. Load Backend Notification Settings
    if (auth.user && auth.user.username) {
        try {
            const res = await fetch(`${API_BASE_URL}/api/notification-settings?username=${auth.user.username}`, {
                 headers: { 
                    'Authorization': `Bearer ${auth.user.token || ''}`
                }
            });
            if (res.ok) {
                const data = await res.json();
                if (data) {
                    telegramConfig.value = {
                        enabled: Boolean(data.telegram_enabled),
                        botToken: data.telegram_bot_token || '',
                        chatId: data.telegram_chat_id || ''
                    };
                    emailConfig.value = {
                        enabled: Boolean(data.email_enabled),
                        smtpHost: data.email_smtp_host || 'smtp.gmail.com',
                        smtpPort: String(data.email_smtp_port || '587'),
                        senderEmail: data.email_sender || '',
                        password: data.email_password || '',
                        recipientEmail: data.email_recipient || ''
                    };
                }
            }
        } catch (e) {
            console.error("Gagal memuat setting backend:", e);
        }
    }

    // Request Notification Permission
    if ("Notification" in window && Notification.permission !== "granted") {
        Notification.requestPermission();
    }
});

const saveBackendSettings = async (type) => {
    if (!auth.user || !auth.user.username) {
        alert("Harap login terlebih dahulu.");
        return;
    }
    
    isLoading.value = true;
    if (type === 'telegram') telegramStatus.value = null;
    if (type === 'email') emailStatus.value = null;

    const payload = {
        username: auth.user.username,
        telegram_enabled: telegramConfig.value.enabled,
        telegram_bot_token: telegramConfig.value.botToken,
        telegram_chat_id: telegramConfig.value.chatId,
        email_enabled: emailConfig.value.enabled,
        email_smtp_host: emailConfig.value.smtpHost,
        email_smtp_port: parseInt(emailConfig.value.smtpPort),
        email_sender: emailConfig.value.senderEmail,
        email_password: emailConfig.value.password,
        email_recipient: emailConfig.value.recipientEmail
    };

    try {
        const response = await fetch(`${API_BASE_URL}/api/notification-settings`, {
            method: 'POST',
            headers: { 
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${auth.user.token}`
            },
            body: JSON.stringify(payload)
        });
        const res = await response.json();
        
        if (res.status === 'saved') {
            if (type === 'telegram') telegramStatus.value = 'success';
            if (type === 'email') emailStatus.value = 'success';
        } else {
            throw new Error(res.error || 'Gagal menyimpan');
        }
    } catch (e) {
        console.error(e);
        if (type === 'telegram') telegramStatus.value = 'error';
        if (type === 'email') emailStatus.value = 'error';
    } finally {
        isLoading.value = false;
    }
};

const testTelegram = async () => {
    if (!telegramConfig.value.botToken || !telegramConfig.value.chatId) {
        alert("Mohon isi Bot Token dan Chat ID terlebih dahulu.");
        return;
    }
    
    // Use local loading state or shared isLoading
    const originalLoading = isLoading.value;
    isLoading.value = true;
    
    try {
        const response = await fetch(`${API_BASE_URL}/api/telegram/test`, {
             method: 'POST',
             headers: { 
                 'Content-Type': 'application/json',
                 'Authorization': `Bearer ${auth.user.token}`
             },
             body: JSON.stringify({ 
                 token: telegramConfig.value.botToken,
                 chat_id: telegramConfig.value.chatId
             })
        });
        const data = await response.json();
        
        if (response.ok) {
            alert(data.message || "Tes berhasil! Cek Telegram Anda.");
        } else {
            alert("Tes Gagal: " + (data.error || "Unknown error"));
        }
    } catch (e) {
        alert("Error koneksi: " + e.message);
    } finally {
        isLoading.value = originalLoading; // Restore or just false
        isLoading.value = false;
    }
};

const saveSuccess = ref(false);

const saveLocalSettings = () => {
    // Save to LocalStorage
    localStorage.setItem('fv_volume', alertConfig.value.volume);
    localStorage.setItem('fv_soundType', alertConfig.value.soundType);
    localStorage.setItem('fv_popup', alertConfig.value.browserPopup);
    localStorage.setItem('fv_sound', alertConfig.value.soundEnabled);
    
    // Update Audio Instance
    alarmAudio.pause();
    alarmAudio.currentTime = 0;
    alarmAudio.src = soundSources[alertConfig.value.soundType] || soundSources.siren1;
    alarmAudio.volume = alertConfig.value.volume / 100;
    
    // Show visual success message
    saveSuccess.value = true;
    setTimeout(() => {
        saveSuccess.value = false;
    }, 3000);
    
    // Notification Feedback
    if (alertConfig.value.browserPopup && "Notification" in window) {
        if (Notification.permission === "granted") {
            new Notification("✅ Pengaturan Disimpan", {
                body: `Volume: ${alertConfig.value.volume}%, Jenis: ${alertConfig.value.soundType}`,
                icon: "/favicon.ico",
                silent: true
            });
        } else if (Notification.permission !== "denied") {
            // Request permission if not denied yet
            Notification.requestPermission().then(permission => {
                if (permission === "granted") {
                    new Notification("✅ Pengaturan Disimpan", {
                       body: `Volume: ${alertConfig.value.volume}%, Jenis: ${alertConfig.value.soundType}`,
                       icon: "/favicon.ico",
                       silent: true
                    });
                }
            });
        } else {
            console.warn("Notification permission denied by user");
        }
    }
    console.log("✅ Settings saved:", { volume: alertConfig.value.volume, sound: alertConfig.value.soundType });

    // Audio Preview
    if (alertConfig.value.soundEnabled) {
        alarmAudio.currentTime = 0;
        alarmAudio.play().catch(e => console.log("Audio preview error:", e));
        setTimeout(() => {
            alarmAudio.pause();
            alarmAudio.currentTime = 0;
        }, 1500);
    }
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
                    <div class="flex gap-2">
                        <input v-model="telegramConfig.botToken" type="text" class="w-full bg-[#151926] border border-gray-700 rounded-lg px-4 py-2.5 text-sm focus:outline-none focus:border-[#2AABEE] transition-colors" placeholder="123456:ABC..." />
                        <button @click="showGuide = !showGuide" class="px-3 py-2 bg-gray-800 hover:bg-gray-700 text-gray-300 rounded-lg text-xs font-semibold transition-colors" title="Cara mendapatkan token">
                           ?
                        </button>
                    </div>
                    
                     <!-- Simple Guide -->
                    <div v-if="showGuide" class="mt-2 p-3 bg-[#151926] border border-gray-700 rounded-lg text-xs text-gray-400 leading-relaxed">
                        <ol class="list-decimal pl-4 space-y-1">
                            <li>Chat <b>@BotFather</b> di Telegram & kirim <code>/newbot</code>.</li>
                            <li>Copy <b>Token</b> yang diberikan ke kolom di atas.</li>
                            <li>Chat bot baru Anda, ketik "Halo".</li>
                            <li>Klik tombol <b>Cek ID</b> di bawah.</li>
                        </ol>
                    </div>
                </div>
                <div>
                    <label class="block text-xs font-semibold text-gray-500 uppercase tracking-wider mb-1">Chat ID</label>
                    <div class="flex gap-2">
                        <input v-model="telegramConfig.chatId" type="text" class="w-full bg-[#151926] border border-gray-700 rounded-lg px-4 py-2.5 text-sm focus:outline-none focus:border-[#2AABEE] transition-colors" placeholder="-100..." />
                        <button @click="checkChatId" :disabled="checkingId || !telegramConfig.botToken" class="whitespace-nowrap px-4 py-2 bg-[#2AABEE]/10 hover:bg-[#2AABEE]/20 text-[#2AABEE] rounded-lg text-xs font-semibold transition-colors disabled:opacity-50">
                            {{ checkingId ? '...' : 'Cek ID' }}
                        </button>
                    </div>
                    <p v-if="idCheckMsg" :class="idCheckSuccess ? 'text-green-500' : 'text-red-500'" class="text-xs mt-1">{{ idCheckMsg }}</p>
                </div>

                <div class="flex items-center justify-between py-2">
                    <span class="text-sm font-medium text-gray-300">Aktifkan Notifikasi</span>
                    <label class="relative inline-flex items-center cursor-pointer">
                        <input type="checkbox" v-model="telegramConfig.enabled" class="sr-only peer">
                        <div class="w-11 h-6 bg-gray-700 peer-focus:outline-none rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:border-gray-300 after:border after:rounded-full after:h-5 after:w-5 after:transition-all peer-checked:bg-[#2AABEE]"></div>
                    </label>
                </div>

                <div class="pt-4 border-t border-gray-800 space-y-3">
                    <button @click="testTelegram" :disabled="isLoading || !telegramConfig.botToken || !telegramConfig.chatId" class="w-full py-2 bg-[#2AABEE]/10 hover:bg-[#2AABEE]/20 text-[#2AABEE] rounded-lg text-sm font-semibold transition-colors flex items-center justify-center gap-2 border border-[#2AABEE]/20">
                         <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M6 9H4.5a2.5 2.5 0 0 1 0-5H6"/><path d="M18 9h1.5a2.5 2.5 0 0 0 0-5H18"/><path d="M4 22h16"/><path d="M10 14.66V17c0 .55-.47.98-.97 1.21C7.85 18.75 7 20.24 7 22"/><path d="M14 14.66V17c0 .55.47.98.97 1.21C16.15 18.75 17 20.24 17 22"/><path d="M18 2H6v7a6 6 0 0 0 12 0V2Z"/></svg>
                         Test Notifikasi
                    </button>

                    <button @click="saveBackendSettings('telegram')" :disabled="isLoading" class="w-full py-2 bg-[#2AABEE] hover:bg-[#2390c8] text-white rounded-lg text-sm font-semibold transition-colors flex items-center justify-center gap-2 shadow-lg shadow-[#2AABEE]/20">
                        <svg v-if="!isLoading" xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M19 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h11l5 5v11a2 2 0 0 1-2 2z"/><polyline points="17 21 17 13 7 13 7 21"/><polyline points="7 3 7 8 15 8"/></svg>
                        <span v-if="isLoading">Menyimpan...</span>
                        <span v-else>Simpan Konfigurasi</span>
                    </button>

                    <p v-if="telegramStatus === 'success'" class="text-green-500 text-xs mt-2 text-center">✓ Data tersimpan</p>
                    <p v-if="telegramStatus === 'error'" class="text-red-500 text-xs mt-2 text-center">Gagal menyimpan. Cek koneksi.</p>
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
                     <button @click="saveBackendSettings('email')" :disabled="isLoading" class="w-full py-2 bg-[#ea4335]/10 hover:bg-[#ea4335]/20 text-[#ea4335] rounded-lg text-sm font-semibold transition-colors flex items-center justify-center gap-2">
                        <svg v-if="!isLoading" xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M19 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h11l5 5v11a2 2 0 0 1-2 2z"/><polyline points="17 21 17 13 7 13 7 21"/><polyline points="7 3 7 8 15 8"/></svg>
                        <span v-if="isLoading">Menyimpan...</span>
                        <span v-else>Simpan Konfigurasi</span>
                    </button>
                    <p v-if="emailStatus === 'success'" class="text-green-500 text-xs mt-2 text-center">✓ Data tersimpan</p>
                    <p v-if="emailStatus === 'error'" class="text-red-500 text-xs mt-2 text-center">Gagal menyimpan. Cek konfigurasi.</p>
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
                    <input type="range" v-model.number="alertConfig.volume" min="0" max="100" class="w-full h-2 bg-gray-700 rounded-lg appearance-none cursor-pointer accent-[#6C4DFF]" />
                </div>

                 <!-- Sound Type -->
                <div>
                    <label class="block text-xs font-semibold text-gray-500 uppercase tracking-wider mb-2">Jenis Suara</label>
                    <select v-model="alertConfig.soundType" class="w-full bg-[#151926] border border-gray-700 rounded-lg px-4 py-2.5 text-sm focus:outline-none focus:border-[#6C4DFF]">
                        <option value="siren1">Siren 1 (Standard)</option>
                        <option value="siren2">Siren 2 (Urgent)</option>
                        <option value="beep">Beep (Subtle)</option>
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
                     <button @click="saveLocalSettings" class="w-full py-2 bg-[#6C4DFF] hover:bg-[#5839ff] text-white rounded-lg text-sm font-semibold transition-colors shadow-lg hover:shadow-[#6C4DFF]/25">
                        Simpan Pengaturan Lokal
                    </button>
                    <p v-if="saveSuccess" class="text-center text-xs text-green-400 mt-2 font-medium animate-pulse">
                        ✓ Data tersimpan
                    </p>
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
