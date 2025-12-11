<script setup>
import { ref, onUnmounted } from 'vue';

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || "http://127.0.0.1:5001";

const props = defineProps({
    maxCameras: {
        type: Number,
        default: 4
    }
});

// Original Data Source
const allCameras = ref([
    { id: 1, name: "Kamera 1", source: "WEBCAM", url: "", isRunning: false, sessionId: null, detections: [] },
    { id: 2, name: "Kamera 2", source: "IP_CAMERA", url: "", isRunning: false, sessionId: null, detections: [] },
    { id: 3, name: "Kamera 3", source: "IP_CAMERA", url: "", isRunning: false, sessionId: null, detections: [] },
    { id: 4, name: "Kamera 4", source: "IP_CAMERA", url: "", isRunning: false, sessionId: null, detections: [] },
]);

// Computed to filter based on prop
import { computed } from 'vue';
const cameras = computed(() => {
    return allCameras.value.slice(0, props.maxCameras);
});

// Poller ID storage
const pollers = {};

// LOAD & SAVE CAMERA NAMES
import { watch, onMounted } from 'vue';

onMounted(() => {
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

    // VALIDATION: Check URL for IP Camera
    if (cam.source === "IP_CAMERA" && !cam.url.trim()) {
        alert("Mohon masukkan URL kamera terlebih dahulu (contoh: http://192.168.1.5:8080/video).");
        return;
    }

    try {
        const userStr = localStorage.getItem("user");
        const user = userStr ? JSON.parse(userStr) : null;
        const username = user?.username || "guest";

        const payload = {
            camera_source: cam.source,
            ip_camera_url: cam.url,
            sensitivity: 70, // default
            username: username
        };

        const response = await fetch(`${API_BASE_URL}/api/start-detection`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
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

        // Start polling detections for this camera
        pollers[cam.id] = setInterval(() => fetchDetections(index), 500);

    } catch (e) {
        console.error(e);
        alert("Error connecting to backend");
    }
};

const stopCamera = async (index) => {
    const cam = cameras.value[index];
    if (!cam.isRunning) return;

    try {
        await fetch(`${API_BASE_URL}/api/stop-detection`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ session_id: cam.sessionId })
        });
    } catch (e) {
        console.error(e);
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
        const res = await fetch(`${API_BASE_URL}/api/detections?session=${cam.sessionId}`);
        if(res.ok) {
            const data = await res.json();
            cam.detections = data.boxes || [];
        }
    } catch (e) {
        // silent
    }
};

const stopAll = () => {
    allCameras.value.forEach((cam, idx) => {
        if (cam.isRunning) stopCamera(idx);
    });
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
                    <img v-if="cam.isRunning && cam.sessionId" 
                         :src="`${API_BASE_URL}/api/video-feed?session=${cam.sessionId}`" 
                         class="video-feed" 
                    />
                    <div v-else class="video-placeholder">
                        <span class="placeholder-text">Camera Offline</span>
                    </div>

                    <!-- Overlay Detections -->
                    <div v-if="cam.isRunning" class="overlay">
                        <div v-for="box in cam.detections" :key="box.id"
                             class="detection-box"
                             :style="{
                                 left: `${box.x}px`,
                                 top: `${box.y}px`,
                                 width: `${box.w}px`,
                                 height: `${box.h}px`
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
