<script setup>
import { ref, onMounted } from 'vue';
import alarmSound from "../assets/alarm.mp3";

const alarmAudio = new Audio(alarmSound);
const volumeAlarm = ref(80);
const soundType = ref("siren1");
const enablePopup = ref(true);
const enableSound = ref(true);

onMounted(() => {
    // Load Local Settings
    const vol = localStorage.getItem('fv_volume');
    if (vol) volumeAlarm.value = Number(vol);
    if(alarmAudio) alarmAudio.volume = volumeAlarm.value / 100;
    
    const popup = localStorage.getItem('fv_popup');
    if (popup) enablePopup.value = (popup === 'true');
    
    const snd = localStorage.getItem('fv_sound');
    if (snd) enableSound.value = (snd === 'true');

    const sType = localStorage.getItem('fv_soundType');
    if (sType) soundType.value = sType;

    // Request Permission if needed
    if ("Notification" in window && Notification.permission !== "granted") {
        Notification.requestPermission();
    }
});

const saveLocalSettings = () => {
    localStorage.setItem('fv_volume', volumeAlarm.value);
    localStorage.setItem('fv_soundType', soundType.value);
    localStorage.setItem('fv_popup', enablePopup.value);
    localStorage.setItem('fv_sound', enableSound.value);
    
    if (alarmAudio) {
        alarmAudio.volume = volumeAlarm.value / 100;
        // Apply Sound Type logic for preview
        if (soundType.value === 'siren2') alarmAudio.playbackRate = 1.5;
        else if (soundType.value === 'beep') alarmAudio.playbackRate = 0.5;
        else alarmAudio.playbackRate = 1.0;
    }
    
    // Notification Feedback
    if ("Notification" in window && Notification.permission === "granted") {
        new Notification("✅ Pengaturan Disimpan", {
            body: `Volume: ${volumeAlarm.value}%, Jenis: ${soundType.value}`,
            icon: "/favicon.ico",
            silent: true
        });
    } else {
        alert("Pengaturan Lokal Disimpan!");
    }

    // Audio Preview
    if (enableSound.value && alarmAudio) {
        alarmAudio.currentTime = 0;
        alarmAudio.play().catch(e => console.log(e));
        setTimeout(() => {
            alarmAudio.pause();
            alarmAudio.currentTime = 0;
        }, 1500);
    }
};
</script>

<template>
    <div class="settings-page">
        <div class="container">
            <h1 class="page-title">Pengaturan Notifikasi</h1>
            <p class="page-subtitle">Kelola preferensi alarm suara dan notifikasi browser Anda</p>

            <div class="settings-panel">
                <div class="panel-header">
                    <h3>🏆 Browser & Suara</h3>
                </div>
                <p class="setting-help" style="margin-bottom: 20px; color: #9ca3af;">
                    Pengaturan notifikasi lokal pada browser dan alarm suara saat halaman dibuka.
                </p>

                <div class="settings-grid">
                    <!-- Volume Slider -->
                    <div class="setting-group">
                        <label class="setting-label">
                            VOLUME ALARM
                            <span class="setting-value">{{ volumeAlarm }}%</span>
                        </label>
                        <input
                            type="range"
                            v-model.number="volumeAlarm"
                            min="0"
                            max="100"
                            class="slider"
                            style="background: #4f46e5;" 
                        />
                    </div>

                    <!-- Sound Type Dropdown -->
                    <div class="setting-group">
                        <label class="setting-label">JENIS SUARA</label>
                        <select v-model="soundType" class="custom-select">
                            <option value="siren1">Siren 1 (Standard)</option>
                            <option value="siren2">Siren 2 (Urgent)</option>
                            <option value="beep">Beep (Subtle)</option>
                        </select>
                    </div>

                    <!-- Notifikasi Popup Toggle -->
                    <div class="setting-group">
                        <div class="setting-row">
                            <div>
                                <label class="setting-label">Notifikasi Popup</label>
                                <p class="setting-help" style="margin:0; font-size:12px; color: #6b7280;">
                                    Tampilkan popup browser saat terminimize
                                </p>
                            </div>
                            <div class="toggle-switch">
                                <input
                                    type="checkbox"
                                    v-model="enablePopup"
                                    class="toggle-input"
                                    id="popup-toggle"
                                />
                                <label for="popup-toggle" class="toggle-label"></label>
                            </div>
                        </div>
                    </div>

                    <!-- Suara Alarm Toggle -->
                    <div class="setting-group">
                        <div class="setting-row">
                            <div>
                                <label class="setting-label">Suara Alarm</label>
                                <p class="setting-help" style="margin:0; font-size:12px; color: #6b7280;">
                                    Mainkan suara saat api terdeteksi
                                </p>
                            </div>
                            <div class="toggle-switch">
                                <input
                                    type="checkbox"
                                    v-model="enableSound"
                                    class="toggle-input"
                                    id="sound-toggle"
                                />
                                <label for="sound-toggle" class="toggle-label"></label>
                            </div>
                        </div>
                    </div>
                </div>

                <button class="save-btn" @click="saveLocalSettings">
                    Simpan Pengaturan Lokal
                </button>
            </div>
        </div>
    </div>
</template>

<style scoped>
.settings-page {
    min-height: 100vh;
    background: #0f0f1e;
    padding: 120px 20px 40px;
    color: white;
}
.container {
    max-width: 800px;
    margin: 0 auto;
}
.page-title {
    font-size: 2.5rem;
    font-weight: 800;
    margin-bottom: 10px;
    text-align: center;
}
.page-subtitle {
    text-align: center;
    color: #9ca3af;
    margin-bottom: 40px;
}

/* Copied Styles */
.settings-panel {
    background: #1a1a2e;
    border-radius: 12px;
    padding: 30px;
    border: 1px solid #2d2d48;
    box-shadow: 0 20px 40px rgba(0,0,0,0.3);
}
.panel-header h3 {
    margin: 0 0 10px 0;
    color: white;
    font-size: 1.5rem;
}
.setting-label {
    display: block;
    font-size: 0.875rem;
    font-weight: 600;
    color: #e5e7eb;
    margin-bottom: 8px;
    text-transform: uppercase;
}
.setting-value {
    color: #8b5cf6;
    margin-left: 8px;
}
.custom-select {
    width: 100%;
    padding: 12px 14px;
    background: #1e293b;
    border: 1px solid #2d3748;
    color: #fff;
    border-radius: 8px;
    margin-bottom: 24px;
    outline: none;
    cursor: pointer;
    font-size: 1rem;
}
.slider {
    width: 100%;
    height: 8px;
    border-radius: 4px;
    background: #1e293b;
    outline: none;
    -webkit-appearance: none;
    appearance: none;
    margin-bottom: 24px;
}
.slider::-webkit-slider-thumb {
    -webkit-appearance: none;
    width: 20px;
    height: 20px;
    border-radius: 50%;
    background: #8b5cf6;
    cursor: pointer;
}
.setting-row {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 24px;
}
.toggle-switch {
    position: relative;
    width: 50px;
    height: 26px;
}
.toggle-input {
    opacity: 0;
    width: 0;
    height: 0;
}
.toggle-label {
    position: absolute;
    cursor: pointer;
    inset: 0;
    background-color: #1e293b;
    transition: 0.3s;
    border-radius: 34px;
}
.toggle-label:before {
    position: absolute;
    content: "";
    height: 20px;
    width: 20px;
    left: 3px;
    bottom: 3px;
    background-color: #6b7280;
    transition: 0.3s;
    border-radius: 50%;
}
.toggle-input:checked + .toggle-label {
    background: #8b5cf6;
}
.toggle-input:checked + .toggle-label:before {
    transform: translateX(24px);
    background-color: #fff;
}
.save-btn {
    width: 100%;
    padding: 16px;
    background: #4f46e5;
    color: #fff;
    font-weight: 700;
    border: none;
    border-radius: 8px;
    cursor: pointer;
    margin-top: 20px;
    font-size: 1rem;
    transition: background 0.3s;
}
.save-btn:hover {
    background: #4338ca;
}
</style>
