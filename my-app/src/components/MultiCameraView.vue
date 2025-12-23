<script setup>
import { ref, onUnmounted } from 'vue';
import alarmSound from "../assets/alarm.mp3";
import { auth } from "../store/auth";

const alarmAudio = new Audio(alarmSound);
alarmAudio.loop = true;

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || "http://127.0.0.1:5000";
const AI_BASE_URL = import.meta.env.VITE_AI_BASE_URL || "http://127.0.0.1:7860";

const props = defineProps({
    maxCameras: {
        type: Number,
        default: 4
    }
});

// Original Data Source - added browser webcam properties
const allCameras = ref([
    { id: 1, name: "Kamera 1", source: "WEBCAM", url: "", isRunning: false, sessionId: null, detections: [], browserStream: null, loopId: null },
    { id: 2, name: "Kamera 2", source: "IP_CAMERA", url: "", isRunning: false, sessionId: null, detections: [], browserStream: null, loopId: null },
    { id: 3, name: "Kamera 3", source: "IP_CAMERA", url: "", isRunning: false, sessionId: null, detections: [], browserStream: null, loopId: null },
    { id: 4, name: "Kamera 4", source: "IP_CAMERA", url: "", isRunning: false, sessionId: null, detections: [], browserStream: null, loopId: null },
]);

// Refs for video and canvas elements (indexed by camera id)
const videoRefs = ref({});
const canvasRefs = ref({});

// Computed to filter based on prop
import { computed, nextTick } from 'vue';
const cameras = computed(() => {
    return allCameras.value.slice(0, props.maxCameras);
});

// Poller ID storage
const pollers = {};

// --- LOCAL SETTINGS ---
const volumeAlarm = ref(80);
const soundType = ref("siren1");
const enablePopup = ref(true);
const enableSound = ref(true);

const saveLocalSettings = () => {
    localStorage.setItem('fv_volume', volumeAlarm.value);
    localStorage.setItem('fv_soundType', soundType.value);
    localStorage.setItem('fv_popup', enablePopup.value);
    localStorage.setItem('fv_sound', enableSound.value);
    
    if (alarmAudio) {
        alarmAudio.volume = volumeAlarm.value / 100;
        
        // Apply Sound Type Logic
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
             // Stop only if no active alarm
             const anyFire = allCameras.value.some(cam => cam.isRunning && cam.detections.length > 0);
             if(!anyFire) {
                alarmAudio.pause();
                alarmAudio.currentTime = 0;
            }
        }, 1500);
    }
};

// LOAD & SAVE CAMERA NAMES & SETTINGS
import { watch, onMounted } from 'vue';

onMounted(async () => {
    // Load Local Settings
    const vol = localStorage.getItem('fv_volume');
    if (vol) volumeAlarm.value = Number(vol);
    if(alarmAudio) alarmAudio.volume = volumeAlarm.value / 100;
    
    const popup = localStorage.getItem('fv_popup');
    if (popup) enablePopup.value = (popup === 'true');
    
    const snd = localStorage.getItem('fv_sound');
    if (snd) enableSound.value = (snd === 'true');

    // Load Sound Type
    const sType = localStorage.getItem('fv_soundType');
    if (sType) {
        soundType.value = sType;
        if (alarmAudio) {
            if (sType === 'siren2') alarmAudio.playbackRate = 1.5;
            else if (sType === 'beep') alarmAudio.playbackRate = 0.5;
            else alarmAudio.playbackRate = 1.0;
        }
    }

    // Setup Notification Permission
    if ("Notification" in window && Notification.permission !== "granted") {
        await Notification.requestPermission();
    }
    
    const userStr = localStorage.getItem("user");

    if (userStr) {
        const user = JSON.parse(userStr);
        const username = user.username || "guest";
        const savedNames = localStorage.getItem(`camera_names_${username}`);
        
        if (savedNames) {
            const names = JSON.parse(savedNames);
            allCameras.value.forEach((cam, index) => {
                if (names[index]) cam.name = names[index];
            });
        }

        // Watch for changes and save (Use allCameras to persist even hidden ones if modified)
        watch(allCameras, (newVal) => {
            const namesToSave = newVal.map(c => c.name);
            localStorage.setItem(`camera_names_${username}`, JSON.stringify(namesToSave));
        }, { deep: true });
    }
});

const startCamera = async (index) => {
    const cam = cameras.value[index];
    if (cam.isRunning) return;

    // WEBCAM mode - use browser webcam capture
    if (cam.source === "WEBCAM") {
        await startBrowserWebcam(index);
        return;
    }

    // VALIDATION: Check URL for IP Camera
    if (cam.source === "IP_CAMERA" && !cam.url.trim()) {
        alert("Mohon masukkan URL kamera terlebih dahulu (contoh: http://192.168.1.5:8080/video).");
        return;
    }

    // IP Camera mode - use server-side detection
    try {
        const userStr = localStorage.getItem("user");
        const user = userStr ? JSON.parse(userStr) : null;
        const username = user?.username || "guest";

        const payload = {
            camera_source: cam.source,
            ip_camera_url: cam.url,
            sensitivity: 70,
            username: username,
            camera_name: cam.name || `Kamera ${cam.id}`
        };

        const token = auth.user?.token || user?.token || '';
        const response = await fetch(`${AI_BASE_URL}/api/start-detection`, {
            method: "POST",
            headers: { 
                "Content-Type": "application/json",
                "Authorization": `Bearer ${token}`
            },
            body: JSON.stringify(payload)
        });

        if (!response.ok) {
            const err = await response.json();
            if (response.status === 403) {
                 alert(err.error || "Limit Camera Reached!");
            } else {
                 alert(`Gagal start kamera ${cam.id}: ${err.error}`);
            }
            return;
        }

        const data = await response.json();
        cam.sessionId = data.session_id;
        cam.isRunning = true;

        pollers[cam.id] = setInterval(() => fetchDetections(index), 500);

    } catch (e) {
        console.error(e);
        alert("Error connecting to backend");
    }
};

// Browser Webcam Mode Functions
const startBrowserWebcam = async (index) => {
    const cam = cameras.value[index];
    
    try {
        cam.isRunning = true;
        cam.detections = [];
        
        await nextTick();
        
        const stream = await navigator.mediaDevices.getUserMedia({
            video: { width: 640, height: 480 },
            audio: false
        });
        
        cam.browserStream = stream;
        
        await nextTick();
        
        const videoEl = videoRefs.value[cam.id];
        if (videoEl) {
            videoEl.srcObject = stream;
            await videoEl.play();
        }
        
        // Start frame processing loop
        startWebcamLoop(index);
        
    } catch (error) {
        console.error("Error accessing webcam:", error);
        cam.isRunning = false;
        
        if (error.name === 'NotAllowedError') {
            alert("Izin kamera ditolak. Mohon berikan izin kamera di browser.");
        } else if (error.name === 'NotFoundError') {
            alert("Webcam tidak ditemukan.");
        } else {
            alert(`Error webcam: ${error.message}`);
        }
    }
};

const startWebcamLoop = (index) => {
    const cam = cameras.value[index];
    
    const processLoop = async () => {
        if (!cam.isRunning || cam.source !== 'WEBCAM') return;
        
        await processWebcamFrame(index);
        
        cam.loopId = setTimeout(() => {
            if (cam.isRunning) {
                requestAnimationFrame(processLoop);
            }
        }, 150); // ~7 FPS to reduce load
    };
    
    requestAnimationFrame(processLoop);
};

const processWebcamFrame = async (index) => {
    const cam = cameras.value[index];
    const videoEl = videoRefs.value[cam.id];
    const canvasEl = canvasRefs.value[cam.id];
    
    if (!videoEl || !canvasEl) return;
    
    const ctx = canvasEl.getContext('2d');
    canvasEl.width = videoEl.videoWidth || 640;
    canvasEl.height = videoEl.videoHeight || 480;
    ctx.drawImage(videoEl, 0, 0, canvasEl.width, canvasEl.height);
    
    const frameData = canvasEl.toDataURL('image/jpeg', 0.7);
    
    try {
        const token = auth.user?.token || '';
        const username = auth.user?.username || 'guest';
        const response = await fetch(`${AI_BASE_URL}/api/process-frame`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${token}`
            },
            body: JSON.stringify({
                frame: frameData,
                sensitivity: 70,
                username: username
            })
        });
        
        if (!response.ok) return;
        
        const data = await response.json();
        
        if (data.success) {
            const frameW = data.frame_width || 640;
            const frameH = data.frame_height || 480;
            
            cam.detections = data.detections.map((d, idx) => ({
                id: idx,
                label: d.class,
                confidence: d.confidence * 100,
                // Convert to percentages for responsive scaling
                left: (d.x / frameW) * 100,
                top: (d.y / frameH) * 100,
                width: (d.w / frameW) * 100,
                height: (d.h / frameH) * 100
            }));
        }
    } catch (error) {
        // Silent
    }
    
    checkAlarmStatus();
};

const stopCamera = async (index) => {
    const cam = cameras.value[index];
    if (!cam.isRunning) return;

    // Stop webcam loop if browser webcam mode
    if (cam.loopId) {
        clearTimeout(cam.loopId);
        cam.loopId = null;
    }
    
    // Stop browser stream if exists
    if (cam.browserStream) {
        cam.browserStream.getTracks().forEach(track => track.stop());
        cam.browserStream = null;
        
        const videoEl = videoRefs.value[cam.id];
        if (videoEl) videoEl.srcObject = null;
    }

    // Stop server session if IP camera mode
    if (cam.sessionId) {
        try {
            const token = auth.user?.token || '';
            await fetch(`${AI_BASE_URL}/api/stop-detection`, {
                method: "POST",
                headers: { 
                    "Content-Type": "application/json",
                    "Authorization": `Bearer ${token}`
                },
                body: JSON.stringify({ session_id: cam.sessionId })
            });
        } catch (e) {
            console.error(e);
        }
    }

    cam.isRunning = false;
    cam.sessionId = null;
    cam.detections = [];
    clearInterval(pollers[cam.id]);
};

const fetchDetections = async (index) => {
    const cam = cameras.value[index];
    if (!cam.sessionId) return;

    try {
        const res = await fetch(`${AI_BASE_URL}/api/detections?session=${cam.sessionId}`);
        if(res.ok) {
            const data = await res.json();
            cam.detections = data.boxes || [];
        }
    } catch (e) {
        // silent
    }
    checkAlarmStatus();
};

const stopAll = () => {
    allCameras.value.forEach((cam, idx) => {
        if (cam.isRunning) stopCamera(idx);
    });
    // Stop audio
    if (!alarmAudio.paused) {
        alarmAudio.pause();
        alarmAudio.currentTime = 0;
    }
};

// ========== SAVE ALARM TO RAILWAY BACKEND ==========
let lastAlarmSaveTime = 0;
const saveAlarmToBackend = async (confidence, cameraName = 'Multi-Camera') => {
    const now = Date.now();
    // Throttle: only save once per 5 seconds
    if (now - lastAlarmSaveTime < 5000) {
        console.log("⏳ Alarm save throttled (5s cooldown)");
        return;
    }
    lastAlarmSaveTime = now;
    
    try {
        const response = await fetch(`${API_BASE_URL}/api/add-alarm`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                camera_id: cameraName,
                confidence: confidence,
                zone: 'Default Zone',
                timestamp: new Date().toISOString().replace('T', ' ').split('.')[0]
            })
        });
        
        if (response.ok) {
            const data = await response.json();
            console.log("💾 Alarm saved to backend:", data);
        } else {
            console.error("❌ Failed to save alarm:", response.status);
        }
    } catch (error) {
        console.error("❌ Error saving alarm to backend:", error);
    }
};

// ========== SEND TELEGRAM NOTIFICATION ==========
let lastTelegramTime = 0;
const sendTelegramNotification = async (cameraName = 'Multi-Camera') => {
    const now = Date.now();
    // Throttle: only send once per 30 seconds
    if (now - lastTelegramTime < 30000) {
        console.log("⏳ Telegram throttled (30s cooldown)");
        return;
    }
    lastTelegramTime = now;
    
    try {
        const token = auth.user?.token || '';
        const response = await fetch(`${API_BASE_URL}/api/send-fire-alert`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${token}`
            },
            body: JSON.stringify({
                camera_name: cameraName,
                message: `🔥 FireVision Alert (${cameraName}) — Api terdeteksi!`
            })
        });
        
        if (response.ok) {
            console.log("📨 Telegram notification sent!");
        } else {
            console.log("⚠️ Telegram notification failed:", response.status);
        }
    } catch (error) {
        console.error("❌ Error sending Telegram:", error);
    }
};

// Check if ANY camera has detections to play sound
// Check if ANY camera has detections to play sound and notify
// Check if ANY camera has detections to play sound and notify
// Uses timestamp persistence to prevent audio stuttering
const checkAlarmStatus = () => {
    const anyFireCamera = allCameras.value.find(cam => cam.isRunning && cam.detections.length > 0);
    const now = Date.now();
    
    // Initialize lastFireTime if not exists
    if (!checkAlarmStatus.lastFireTime) checkAlarmStatus.lastFireTime = 0;

    if (anyFireCamera) {
        // Update last time fire was seen
        checkAlarmStatus.lastFireTime = now;

        // 🚀 Save alarm to Railway backend (throttled to 5s)
        const avgConfidence = anyFireCamera.detections.length > 0
            ? anyFireCamera.detections.reduce((sum, d) => sum + (d.confidence || 0), 0) / anyFireCamera.detections.length
            : 85;
        saveAlarmToBackend(avgConfidence, anyFireCamera.name || 'Multi-Camera');
        
        // Note: Telegram notification handled by ai_service internally via /api/process-frame
        // sendTelegramNotification disabled due to CORS issues with separate backend

        // Audio
        if (enableSound.value) {
            if (alarmAudio.paused) {
                alarmAudio.volume = volumeAlarm.value / 100;
                alarmAudio.play().catch(e => console.warn("Audio play blocked", e));
            }
        } else {
             // If sound disabled but playing, stop it
             if (!alarmAudio.paused) {
                alarmAudio.pause();
                alarmAudio.currentTime = 0;
            }
        }
        
        // Browser Notification
        if (enablePopup.value && "Notification" in window && Notification.permission === "granted") {
            if (!checkAlarmStatus.lastNotify || now - checkAlarmStatus.lastNotify > 5000) {
                new Notification("🔥 PERINGATAN API!", {
                    body: `Api terdeteksi di ${anyFireCamera.name || 'Kamera ' + anyFireCamera.id}! Segera periksa!`,
                    icon: "/favicon.ico"
                });
                checkAlarmStatus.lastNotify = now;
            }
        }
    } else {
        // No fire currently detected
        // Only stop audio if fire has been lost for > 3 seconds (3000ms)
        if (now - checkAlarmStatus.lastFireTime > 3000) {
            if (!alarmAudio.paused) {
                alarmAudio.pause();
                alarmAudio.currentTime = 0;
            }
        }
    }
};

onUnmounted(() => {
    stopAll();
});
</script>

<template>
    <div class="multi-camera-container">
        <h2 class="title">Multi-Camera Monitor ({{ maxCameras }} Channels)</h2>
        
        <div class="grid-container">
            <div v-for="(cam, index) in cameras" :key="cam.id" class="camera-card">
                <div class="card-header">
                    <input type="text" v-model="cam.name" class="camera-name-input" placeholder="Nama Kamera..." />
                    <div class="status-indicator" :class="{ active: cam.isRunning }"></div>
                </div>

                <div class="video-window">
                    <!-- Hidden Canvas for Frame Capture -->
                    <canvas :ref="el => { if (el) canvasRefs[cam.id] = el }" style="display: none;"></canvas>
                    
                    <!-- Browser Webcam Video -->
                    <video v-if="cam.isRunning && cam.source === 'WEBCAM'"
                           :ref="el => { if (el) videoRefs[cam.id] = el }"
                           class="video-feed"
                           autoplay muted playsinline
                    ></video>
                    <!-- IP Camera Stream -->
                    <img v-else-if="cam.isRunning && cam.sessionId" 
                         :src="`${AI_BASE_URL}/api/video-feed?session=${cam.sessionId}`" 
                         class="video-feed" 
                    />
                    <!-- Offline Placeholder -->
                    <div v-else class="video-placeholder">
                        <span class="placeholder-text">Camera Offline</span>
                    </div>

                    <!-- Overlay Detections -->
                    <div v-if="cam.isRunning" class="overlay">
                        <div v-for="box in cam.detections" :key="box.id"
                             class="detection-box"
                             :style="{
                                 left: `${box.left}%`,
                                 top: `${box.top}%`,
                                 width: `${box.width}%`,
                                 height: `${box.height}%`
                             }">
                             <span class="label">{{ box.label }} {{ Math.round(box.confidence) }}%</span>
                        </div>
                    </div>
                </div>

                <div class="controls">
                    <div class="input-group">
                        <select v-model="cam.source" :disabled="cam.isRunning">
                            <option value="WEBCAM">Webcam Device</option>
                            <option value="IP_CAMERA">IP Camera URL</option>
                        </select>
                    </div>
                    
                    <div class="input-group" v-if="cam.source === 'IP_CAMERA'">
                        <input type="text" v-model="cam.url" placeholder="http://192.168.x.x:port/video" :disabled="cam.isRunning" />
                    </div>

                    <button v-if="!cam.isRunning" @click="startCamera(index)" class="btn start">Start</button>
                    <button v-else @click="stopCamera(index)" class="btn stop">Stop</button>
                </div>
            </div>
        </div>



    </div>
</template>

<style scoped>
/* SETTINGS PANEL STYLES */
.settings-panel-container {
    max-width: 1400px;
    margin: 40px auto;
    padding: 0 20px;
}
.settings-panel {
    background: #1a1a2e;
    border-radius: 12px;
    padding: 24px;
    border: 1px solid #2d2d48;
}
.panel-header h3 {
    margin: 0 0 10px 0;
    color: white;
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
    padding: 10px 14px;
    background: #1e293b;
    border: 1px solid #2d3748;
    color: #fff;
    border-radius: 8px;
    margin-bottom: 16px;
    outline: none;
    cursor: pointer;
}
.slider {
    width: 100%;
    height: 8px;
    border-radius: 4px;
    background: #1e293b;
    outline: none;
    -webkit-appearance: none;
    appearance: none;
    margin-bottom: 20px;
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
    margin-bottom: 20px;
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
    padding: 14px;
    background: #1f2937;
    color: #fff;
    font-weight: 600;
    border: none;
    border-radius: 8px;
    cursor: pointer;
    margin-top: 10px;
}
.save-btn:hover {
    background: #374151;
}

/* Existing Styles */
.multi-camera-container {
    padding: 20px;
    background: #0f0f1e;
    min-height: 100vh;
    color: white;
}

.title {
    text-align: center;
    margin-bottom: 30px;
    font-size: 2rem;
    font-weight: bold;
}

.grid-container {
    display: grid;
    grid-template-columns: repeat(2, 1fr);
    gap: 20px;
    max-width: 1400px;
    margin: 0 auto;
}

.camera-card {
    background: #1a1a2e;
    border-radius: 12px;
    padding: 15px;
    border: 1px solid #2d2d48;
}

.card-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 10px;
}

.camera-name-input {
    background: transparent;
    border: none;
    border-bottom: 2px solid transparent;
    color: white;
    font-size: 1.17em;
    font-weight: bold;
    width: 70%;
    padding: 4px 0;
    transition: all 0.3s ease;
}

.camera-name-input:focus, 
.camera-name-input:hover {
    border-bottom-color: #8b5cf6;
    outline: none;
}

.status-indicator {
    width: 10px;
    height: 10px;
    border-radius: 50%;
    background: #ef4444;
}
.status-indicator.active {
    background: #22c55e;
    box-shadow: 0 0 10px #22c55e;
}

.video-window {
    position: relative;
    width: 100%;
    height: 300px;
    background: #000;
    border-radius: 8px;
    overflow: hidden;
    margin-bottom: 15px;
}

.video-feed {
    width: 100%;
    height: 100%;
    object-fit: cover;
}

.video-placeholder {
    width: 100%;
    height: 100%;
    display: flex;
    align-items: center;
    justify-content: center;
    background: #111;
    color: #555;
    border: 1px dashed #333;
}

.controls {
    display: flex;
    flex-direction: column;
    gap: 10px;
}

.input-group select, .input-group input {
    width: 100%;
    padding: 8px;
    background: #2d2d48;
    border: 1px solid #3f3f5f;
    color: white;
    border-radius: 6px;
}

.btn {
    padding: 10px;
    border: none;
    border-radius: 6px;
    cursor: pointer;
    font-weight: bold;
    color: white;
    transition: all 0.2s;
}

.btn.start {
    background: #8b5cf6;
}
.btn.start:hover {
    background: #7c3aed;
}

.btn.stop {
    background: #ef4444;
}
.btn.stop:hover {
    background: #dc2626;
}

.overlay {
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    pointer-events: none;
}

/* Note: Detection boxes coordinates from backend need scaling if video is object-fit: cover
   For simplicity assume raw pixels or update boxToStyle logic similar to DemoFire.vue 
   if precise alignment is needed. backend sends raw pixels from 640x480 frame.
   Ideally we should normalize. For this prototype we will trust CSS scaling or adjust later.
   Actually, the simplistic style binding below expects exact pixels which might mismatch if resized.
   Better approach: Use percentage.
*/

.detection-box {
    position: absolute;
    border: 2px solid red;
}
.label {
    position: absolute;
    top: -20px;
    left: 0;
    background: red;
    color: white;
    font-size: 10px;
    padding: 2px 4px;
}

@media (max-width: 768px) {
    .grid-container {
        grid-template-columns: 1fr;
    }
}
</style>
