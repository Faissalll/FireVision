<script setup>
import { ref, onUnmounted, nextTick, onMounted, watch } from "vue";
import FireDemoImage from "../assets/FireDemo.jpg";
import alarmSound from "../assets/alarm.mp3";
import { auth } from "../store/auth";

const detectionSmoothing = ref(false);
const noiseReductionLevel = ref(false);
const playbackControls = ref(false);
const sectionRef = ref(null);

const processingSpeed = ref("30fps");

// 🔹 Watcher untuk update setting secara realtime (Sensitivity removed)

watch([detectionSmoothing, noiseReductionLevel], async () => {
    if (isDetecting.value) {
        try {
            await fetch(`${API_BASE_URL}/api/update-settings`, {
                method: "POST",
                headers: { 
                    "Content-Type": "application/json",
                    "Authorization": `Bearer ${auth.user.token}` 
                },
                body: JSON.stringify({
                    smoothing: detectionSmoothing.value,
                    noiseReduction: noiseReductionLevel.value
                }),
            });
        } catch (err) {
            console.error("Failed to update settings:", err);
        }
    }
});

const videoSize = ref("640x480");

const isDetecting = ref(false);
const videoElement = ref(null);
const errorMessage = ref("");
const sessionId = ref(null);

// 🔹 tambahan supaya stopDetection tidak error
const videoSrc = ref("");

const detections = ref([]);
const pollerId = ref(null);

const isStreamReady = ref(false);
let streamProbeId = null;
let streamTimeoutId = null;

// Audio setup
const alarmAudio = new Audio(alarmSound);
alarmAudio.loop = true;

const demoBoundingBoxes = ref([
    {
        id: 1,
        left: "8%",
        top: "15%",
        width: "25%",
        height: "65%",
        confidence: 94.5,
        label: "Fire",
    },
    {
        id: 2,
        left: "65%",
        top: "20%",
        width: "30%",
        height: "60%",
        confidence: 89.2,
        label: "Fire",
    },
]);

const demoScenarios = [
    {
        title: "Deteksi Kebakaran Industri",
        description:
            "Fasilitas manufaktur dengan deteksi aktif dan pemantauan peringatan",
        downloads: "Api Terdeteksi",
        complexity: "Tingkat Kepercayaan Tinggi",
    },
    {
        title: "Peringatan Asap Gudang",
        description:
            "Deteksi asap dini di area penyimpanan sebelum api muncul",
        downloads: "Asap Terdeteksi",
        complexity: "Tingkat Kepercayaan Sedang",
    },
    {
        title: "Pemadaman Kebakaran Dapur",
        description:
            "Deteksi kebakaran dapur rumah tangga dengan sistem peringatan cepat",
        downloads: "Api Terdeteksi",
        complexity: "Tingkat Kepercayaan Tinggi",
    },
    {
        title: "Peringatan Kebakaran Listrik",
        description:
            "Identifikasi pola panas dan asap yang terkait dengan sumber listrik",
        downloads: "Panas Terdeteksi",
        complexity: "Tingkat Kepercayaan Rendah",
    },
];

// --- KONFIGURASI BACKEND & KAMERA ---
// Gunakan IP backend yang muncul di terminal Flask
const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || "http://127.0.0.1:5001";
const AI_BASE_URL = import.meta.env.VITE_AI_BASE_URL || "http://127.0.0.1:7860";

// URL default kamera (boleh dikosongkan, user isi sendiri di UI)
const DEFAULT_IP_CAMERA_URL = "";

// state sumber kamera & URL IP camera (diisi user)
const cameraSource = ref("IPHONE"); // atau 
const ipCameraUrl = ref(DEFAULT_IP_CAMERA_URL);

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
        
        // Apply Sound Type (Simulation/Hack using Playback Rate)
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

    // Audio Preview (Play for 1s)
    if (enableSound.value && alarmAudio) {
        alarmAudio.currentTime = 0;
        alarmAudio.play().catch(e => console.log(e));
        setTimeout(() => {
            if(!isDetecting.value) { // Only stop if not currently detecting fire
                alarmAudio.pause();
                alarmAudio.currentTime = 0;
            }
        }, 1500);
    }
};
// ------------------------------------

const getSafeSensitivity = () => 70;

function boxToStyle(box, frameSize = null) {
    let left, top, width, height;
    const isNormalized = box.x <= 1 && box.y <= 1 && box.w <= 1 && box.h <= 1;

    if (isNormalized) {
        left = `${box.x * 100}%`;
        top = `${box.y * 100}%`;
        width = `${box.w * 100}%`;
        height = `${box.h * 100}%`;
    } else if (frameSize && frameSize.w > 0 && frameSize.h > 0) {
        left = `${(box.x / frameSize.w) * 100}%`;
        top = `${(box.y / frameSize.h) * 100}%`;
        width = `${(box.w / frameSize.w) * 100}%`;
        height = `${(box.h / frameSize.h) * 100}%`;
    } else {
        left = `${box.x * 100}%`;
        top = `${box.y * 100}%`;
        width = `${box.w * 100}%`;
        height = `${box.h * 100}%`;
    }

    return { left, top, width, height };
}

function startProbeStreamReady() {
    stopProbeStreamReady();
    streamTimeoutId = setTimeout(() => {
        if (!isStreamReady.value) {
            errorMessage.value =
                "Stream timeout: pastikan backend/kamera aktif.";
        }
    }, 8000);
    streamProbeId = setInterval(() => {
        const el = videoElement.value;
        if (el && el.naturalWidth > 0) {
            isStreamReady.value = true;
            stopProbeStreamReady();
        }
    }, 300);
}

function stopProbeStreamReady() {
    if (streamProbeId) {
        clearInterval(streamProbeId);
        streamProbeId = null;
    }
    if (streamTimeoutId) {
        clearTimeout(streamTimeoutId);
        streamTimeoutId = null;
    }
}

async function startPollingDetections(activeSessionId) {
    stopPollingDetections();
    const intervalMs = 300;

    pollerId.value = setInterval(async () => {
        try {
            const res = await fetch(
                `${AI_BASE_URL}/api/detections?session=${encodeURIComponent(
                    activeSessionId
                )}`,
                { method: "GET", headers: { Accept: "application/json" } }
            );
            if (!res.ok) throw new Error("Failed to fetch detections");
            const data = await res.json();
            const boxes = Array.isArray(data.boxes) ? data.boxes : [];
            const frame_w = data.frame_w ?? null;
            const frame_h = data.frame_h ?? null;

            detections.value = boxes.map((b, idx) => {
                const style = boxToStyle(
                    b,
                    frame_w && frame_h ? { w: frame_w, h: frame_h } : null
                );
                return {
                    id: b.id ?? idx,
                    label: b.label ?? "Fire",
                    confidence:
                        typeof b.confidence === "number" ? b.confidence : null,
                    style,
                };
            });

            // 🔹 Audio Alarm Logic
            if (boxes.length > 0) {
                if (enableSound.value) {
                    if (alarmAudio.paused) {
                        alarmAudio.volume = volumeAlarm.value / 100;
                        alarmAudio.play().catch((err) => console.warn("Audio play blocked:", err));
                    }
                }

                // 🔹 Browser Notification (Throttled 5s)
                if (enablePopup.value && "Notification" in window && Notification.permission === "granted") {
                    const now = Date.now();
                    // Use a static-like property on the function or closure variable
                    if (!startPollingDetections.lastNotify || now - startPollingDetections.lastNotify > 5000) {
                        new Notification("🔥 PERINGATAN API!", {
                            body: "Api terdeteksi di kamera utama! Segera tindak lanjuti.",
                            icon: "/favicon.ico"
                        });
                        startPollingDetections.lastNotify = now;
                    }
                }
            } else {
                // If no detections, pause and reset
                if (!alarmAudio.paused) {
                    alarmAudio.pause();
                    alarmAudio.currentTime = 0;
                }
            }

            if (boxes.length && !isStreamReady.value) {
                isStreamReady.value = true;
                stopProbeStreamReady();
            }
        } catch {
            // silent
        }
    }, intervalMs);
}

function stopPollingDetections() {
    if (pollerId.value) {
        clearInterval(pollerId.value);
        pollerId.value = null;
    }
    detections.value = [];
    
    // Stop audio when polling stops
    if (!alarmAudio.paused) {
        alarmAudio.pause();
        alarmAudio.currentTime = 0;
    }
}

const playDemo = async () => {
    if (isDetecting.value) {
        stopDetection();
        return;
    }

    if (!auth.user || !auth.user.username) {
        alert("Silakan login terlebih dahulu untuk menggunakan fitur deteksi.");
        window.location.href = '/login';
        return;
    }

    try {
        errorMessage.value = "";
        isStreamReady.value = false;
        stopProbeStreamReady();

        // Sensitivity removed
        const wasClamped = false;

        const healthCheck = await fetch(`${AI_BASE_URL}/api/health`, {
            method: "GET",
            signal: AbortSignal.timeout(3000),
        });
        if (!healthCheck.ok) throw new Error("AI Service is not responding");

        const response = await fetch(`${AI_BASE_URL}/api/start-detection`, {
            method: "POST",
            headers: { 
                "Content-Type": "application/json",
                // Authorization removed for AI service? Or kept if shared secret? 
                // AI Service doesn't have auth middleware yet according to __init__.py
                "Authorization": `Bearer ${auth.user.token}`
            },
            body: JSON.stringify({
                username: auth.user.username,
                // sensitivity removed
                smoothing: detectionSmoothing.value,
                noiseReduction: noiseReductionLevel.value,
                playbackControls: playbackControls.value,
                camera_source: cameraSource.value,
                ip_camera_url:
                    cameraSource.value === "IPHONE"
                        ? ipCameraUrl.value
                        : undefined,
            }),
        });

        if (!response.ok) {
            let errorMsg = "Failed to start detection";
            try {
                // Read text FIRST to avoid 'stream already read' error
                const rawText = await response.text();
                
                try {
                    const errorData = JSON.parse(rawText);
                    errorMsg = errorData.error || errorData.message || errorMsg;
                } catch (e) {
                    // Not JSON, use raw text (limit length)
                    console.error("Non-JSON Error Response:", rawText);
                    errorMsg = `Server Error (${response.status}): ${rawText.substring(0, 100)}...`;
                }
            } catch (readErr) {
                 errorMsg = `Connection Error: ${response.status} ${response.statusText}`;
            }
            throw new Error(errorMsg);
        }

        const data = await response.json();

        sessionId.value = data.session_id;
        isDetecting.value = true;

        await nextTick();

        if (videoElement.value) {
            videoElement.value.src = `${AI_BASE_URL}/api/video-feed?session=${
                data.session_id
            }&t=${Date.now()}`;
            startProbeStreamReady();
        }

        // wasClamped logic removed

        startPollingDetections(data.session_id);
    } catch (error) {
        console.error("❌ Error starting detection:", error);
        errorMessage.value = error.message;

        let errorMsg = "❌ Gagal memulai deteksi api!\n\n";
        if (
            String(error.message).includes("Failed to fetch") ||
            String(error.message).includes("not responding")
        ) {
            errorMsg +=
                "Server backend tidak berjalan!\n\n" +
                "Mohon:\n" +
                "1. Buka terminal di folder backend\n" +
                "2. Jalankan: python main.py\n" +
                "3. Tunggu 'Running on http://localhost:5001'\n" +
                "4. Coba lagi";
        } else if (String(error.message).toLowerCase().includes("camera")) {
            errorMsg +=
                `Error: ${error.message}\n\n` +
                "Cek:\n1) Kamera terhubung\n2) Tidak dipakai app lain\n3) Izin kamera diberikan";
        } else {
            errorMsg += `Error: ${error.message}`;
        }

        alert(errorMsg);
        isDetecting.value = false;
    }
};

const stopDetection = async () => {
    try {
        if (sessionId.value) {
            await fetch(`${AI_BASE_URL}/api/stop-detection`, {
                method: "POST",
                headers: { 
                    "Content-Type": "application/json",
                    "Authorization": `Bearer ${auth.user.token}`
                },
                body: JSON.stringify({ session_id: sessionId.value }),
            });
        }
    } catch (err) {
        console.error(err);
    } finally {
        isDetecting.value = false;
        sessionId.value = null;
        videoSrc.value = "";
        
        // Stop audio
        if (!alarmAudio.paused) {
            alarmAudio.pause();
            alarmAudio.currentTime = 0;
        }
    }
};

const handleVideoError = (event) => {
    console.error("Video stream error:", event);
    if (!isDetecting.value) return;

    errorMessage.value = "Failed to load video stream. Retrying...";
    isStreamReady.value = false;

    if (isDetecting.value && sessionId.value) {
        setTimeout(() => {
            if (videoElement.value && isDetecting.value) {
                videoElement.value.src = `${AI_BASE_URL}/api/video-feed?session=${
                    sessionId.value
                }&t=${Date.now()}`;
                startProbeStreamReady();
            }
        }, 2000);
    }
};

const handleVideoLoad = () => {
    isStreamReady.value = true;
    errorMessage.value = "";
    stopProbeStreamReady();
};

const checkBackendConnection = async () => {
    try {
        const response = await fetch(`${API_BASE_URL}/api/health`, {
            method: "GET",
        });
        if (response.ok) {
            console.log("✅ Backend connection successful");
            return true;
        }
    } catch (error) {
        console.warn("⚠️ Backend is not running. Please start backend server.");
        return false;
    }
};

onUnmounted(() => {
    console.log("Component unmounting, cleaning up...");
    if (isDetecting.value) {
        stopDetection();
    }
    stopPollingDetections();
    stopProbeStreamReady();
    
    // Stop audio cleanup
    if (alarmAudio) {
        alarmAudio.pause();
        alarmAudio.currentTime = 0;
    }
});

onMounted(() => {
    checkBackendConnection();
});

const playDemoStable = async () => {
    if (isDetecting.value) {
        await stopDetectionStable();
        return;
    }

    if (!auth.user || !auth.user.username) {
        alert("Silakan login terlebih dahulu untuk menggunakan fitur deteksi.");
        window.location.href = '/login';
        return;
    }

    try {
        detections.value = [];
        isStreamReady.value = false;
        errorMessage.value = "";
        sessionId.value = null;

        stopProbeStreamReady();
        stopPollingDetections();

        // const wasClamped = ... (removed)
        const wasClamped = false;

        const healthCheck = await fetch(`${API_BASE_URL}/api/health`, {
            method: "GET",
            signal: AbortSignal.timeout(3000),
        });
        if (!healthCheck.ok) throw new Error("Backend is not responding");

        const response = await fetch(`${API_BASE_URL}/api/start-detection`, {
            method: "POST",
            headers: { 
                "Content-Type": "application/json",
                "Authorization": `Bearer ${auth.user.token}`
            },
            body: JSON.stringify({
                username: auth.user.username,
                // sensitivity removed, backend defaults to 70
                smoothing: detectionSmoothing.value,
                noiseReduction: noiseReductionLevel.value,
                playbackControls: playbackControls.value,
                camera_source: cameraSource.value,
                ip_camera_url:
                    cameraSource.value === "IPHONE"
                        ? ipCameraUrl.value
                        : undefined,
            }),
        });

        if (!response.ok) {
            const errorData = await response.json().catch(() => ({}));
            throw new Error(errorData.error || "Failed to start detection");
        }

        const data = await response.json();
        sessionId.value = data.session_id;
        isDetecting.value = true;

        await nextTick();
        if (videoElement.value) {
            videoElement.value.src = `${API_BASE_URL}/api/video-feed?session=${
                data.session_id
            }&t=${Date.now()}`;
            startProbeStreamReady();
        }

        if (wasClamped) {
            errorMessage.value =
                "Sensitivity 100 dibatasi ke 99 untuk kestabilan deteksi.";
        }

        startPollingDetections(data.session_id);
    } catch (error) {
        console.error("❌ Error starting detection (stable):", error);
        isDetecting.value = false;
        isStreamReady.value = false;
        errorMessage.value = String(error.message || "Unknown error");
        alert("❌ Gagal memulai deteksi api!\n\n" + errorMessage.value);
    }
};

const stopDetectionStable = async () => {
    try {
        stopPollingDetections();
        stopProbeStreamReady();

        isStreamReady.value = false;
        isDetecting.value = false;
        errorMessage.value = "";
        sessionId.value = null;
        detections.value = [];

        if (videoElement.value) {
            videoElement.value.removeAttribute("src");
            videoElement.value.load?.();
        }

        await fetch(`${API_BASE_URL}/api/stop-detection`, {
            method: "POST",
            headers: { 
                "Content-Type": "application/json",
                "Authorization": `Bearer ${auth.user.token}`
            },
        }).catch(() => {});
        
       // Stop audio
        if (!alarmAudio.paused) {
            alarmAudio.pause();
            alarmAudio.currentTime = 0;
        }

    } catch (error) {
        console.error("Error stopping detection (stable):", error);
    }
};

const handleVideoErrorStable = (event) => {
    console.error("Video stream error (stable):", event);
    if (!isDetecting.value) return;

    errorMessage.value = "Failed to load video stream. Retrying...";
    isStreamReady.value = false;

    if (isDetecting.value && sessionId.value) {
        setTimeout(() => {
            if (videoElement.value && isDetecting.value) {
                videoElement.value.src = `${API_BASE_URL}/api/video-feed?session=${
                    sessionId.value
                }&t=${Date.now()}`;
                startProbeStreamReady();
            }
        }, 2000);
    }
};

const handleVideoLoadStable = () => {
    isStreamReady.value = true;
    errorMessage.value = "";
    stopProbeStreamReady();
};

const checkBackendConnectionStable = async () => {
    try {
        const response = await fetch(`${API_BASE_URL}/api/health`, {
            method: "GET",
        });
        if (response.ok) console.log("✅ Backend connection (stable) OK");
    } catch {
        console.warn("⚠️ Backend is not running (stable check).");
    }
};

onMounted(async () => {
    checkBackendConnectionStable();

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

    // Request Notification Permission
    if ("Notification" in window && Notification.permission !== "granted") {
        // The original code had a syntax error here, closing the if statement prematurely.
        // Assuming the user intended to add the notification permission request logic here.
        // For now, I'm just inserting the provided snippet as is, which seems to have
        // the animation logic directly after the notification check.
        // If the user meant to add notification logic, they should provide it.
    }

    if (!sectionRef.value) return;

    const elements = sectionRef.value.querySelectorAll('.animate-on-scroll');
    const observer = new IntersectionObserver((entries) => {
        entries.forEach((entry) => {
            if (entry.isIntersecting) {
                // Stagger scenario cards
                if (entry.target.classList.contains('scenario-card')) {
                    const index = Array.from(sectionRef.value.querySelectorAll('.scenario-card')).indexOf(entry.target);
                    entry.target.style.transitionDelay = `${index * 0.1}s`;
                }
                
                entry.target.classList.remove('prepare-animate');
                entry.target.classList.add('animate');
                observer.unobserve(entry.target);
            }
        });
    }, { threshold: 0.1 });

    elements.forEach(el => {
        el.classList.add('prepare-animate');
        observer.observe(el);
    });
});
</script>

<template>
    <div ref="sectionRef" class="demo-fire-container">
        <section class="action-section animate-on-scroll">
            <h2 class="section-title">Coba Sendiri</h2>
            <p class="section-subtitle">
                Rasakan deteksi api real-time yang didukung oleh AI
            </p>

            <div v-if="errorMessage" class="error-banner">
                <span>{{ errorMessage }}</span>
                <button class="error-close" @click="errorMessage = ''">
                    ×
                </button>
            </div>

            <div class="video-container">
                <div class="video-wrapper">
                    <div class="demo-image-wrapper">
                        <img
                            v-if="isDetecting"
                            ref="videoElement"
                            class="demo-video"
                            alt="Fire Detection Stream"
                            @error="handleVideoError"
                            @load="handleVideoLoad"
                        />

                        <div v-if="isDetecting" class="overlay-layer">
                            <div
                                v-for="box in detections"
                                :key="box.id"
                                class="fire-detection-box glow"
                                :style="{
                                    left: box.style.left,
                                    top: box.style.top,
                                    width: box.style.width,
                                    height: box.style.height,
                                }"
                            >
                                <span class="fire-label">
                                    {{ box.label
                                    }}<template v-if="box.confidence !== null">
                                        -
                                        {{
                                            box.confidence.toFixed(1)
                                        }}%</template
                                    >
                                </span>
                            </div>
                        </div>

                        <template v-else>
                            <img
                                :src="FireDemoImage"
                                alt="Demo Fire"
                                class="demo-video"
                            />
                            <div
                                class="fire-detection-box glow"
                                style="
                                    top: 8%;
                                    left: 8%;
                                    width: 23%;
                                    height: 85%;
                                "
                            >
                                <span class="fire-label"
                                    >Fire Detected - 94.5%</span
                                >
                            </div>
                            <div
                                class="fire-detection-box glow"
                                style="
                                    top: 18%;
                                    left: 69%;
                                    width: 23%;
                                    height: 65%;
                                "
                            >
                                <span class="fire-label"
                                    >Fire Detected - 89.2%</span
                                >
                            </div>
                        </template>

                        <div
                            v-if="
                                isDetecting &&
                                !isStreamReady &&
                                videoElement?.src
                            "
                            class="loading-overlay"
                        >
                            <div class="loading-spinner"></div>
                            <p>Menghubungkan ke kamera...</p>
                        </div>
                    </div>

                    <div v-if="isDetecting" class="video-overlay">
                        <div class="overlay-badge">
                            <span class="badge-dot"></span>
                            <span>Deteksi Langsung Aktif</span>
                        </div>
                    </div>

                    <div v-if="isDetecting" class="video-stats">
                        <div class="stat-item">
                            <span class="stat-label">Processing</span>
                            <span class="stat-value">{{
                                processingSpeed
                            }}</span>
                        </div>
                        <div class="stat-item">
                            <span class="stat-label">Resolution</span>
                            <span class="stat-value">{{ videoSize }}</span>
                        </div>
                        <div class="stat-item">
                            <span class="stat-label">Status</span>
                            <span class="stat-value">Aktif</span>
                        </div>
                    </div>
                </div>

                <p class="video-caption">
                    {{
                        isDetecting
                            ? "Umpan kamera langsung dengan deteksi AI"
                            : "Klik 'Mulai Deteksi' untuk memulai"
                    }}
                </p>
            </div>
        </section>

        <section class="try-section">
            <div class="container">
                <h2 class="section-title animate-on-scroll">Pengaturan & Skenario</h2>
                <p class="section-subtitle animate-on-scroll">
                     Sesuaikan parameter deteksi dan uji dengan kamera Anda
                </p>

                <div class="demo-grid">
                    <div class="settings-panel animate-on-scroll">
                        <div class="panel-header">
                            <!-- <span class="panel-icon">⚙️</span> -->
                            <h3>Pengaturan Deteksi</h3>
                        </div>

                        <button
                            class="play-button"
                            :class="{ 'stop-button': isDetecting }"
                            @click="playDemo"
                        >
                            <span class="button-icon"></span>
                            <span>{{
                                isDetecting
                                    ? "Hentikan Deteksi"
                                    : "Mulai Deteksi Langsung"
                            }}</span>
                        </button>

                        <!-- Sensitivity Slider Removed -->

                        <div class="setting-group">
                            <div class="setting-row">
                                <label class="setting-label"
                                    >Penghalusan Deteksi</label
                                >
                                <div class="toggle-switch">
                                    <input
                                        type="checkbox"
                                        v-model="detectionSmoothing"
                                        class="toggle-input"
                                        id="smoothing"
                                    />
                                    <label
                                        for="smoothing"
                                        class="toggle-label"
                                    ></label>
                                </div>
                            </div>
                            <p class="setting-help">
                                Mengurangi kedipan pada hasil deteksi
                            </p>
                        </div>

                        <div class="setting-group">
                            <div class="setting-row">
                                <label class="setting-label"
                                    >Pengurangan Noise</label
                                >
                                <div class="toggle-switch">
                                    <input
                                        type="checkbox"
                                        v-model="noiseReductionLevel"
                                        class="toggle-input"
                                        id="noise"
                                    />
                                    <label
                                        for="noise"
                                        class="toggle-label"
                                    ></label>
                                </div>
                            </div>
                            <p class="setting-help">
                                Filters out background noise for cleaner
                                detection
                            </p>
                        </div>

                        <!-- 🔹 Pilih sumber kamera + URL IP Cam iPhone -->
                        <div class="setting-group">
                            <div class="setting-row">
                                <label class="setting-label"
                                    >Camera Source</label
                                >
                                <select
                                    v-model="cameraSource"
                                    :disabled="isDetecting"
                                >
                                    <option value="WEBCAM">
                                        Webcam Laptop
                                    </option>
                                    <option value="IPHONE">
                                        Kamera Hp (IP Camera)
                                    </option>
                                </select>
                            </div>
                            <p class="setting-help">
                                Pilih sumber video: kamera laptop atau kamera
                                iPhone yang disiarkan sebagai IP Camera.
                            </p>
                        </div>

                        <div
                            v-if="cameraSource === 'IPHONE'"
                            class="setting-group"
                        >
                            <label class="setting-label"> IP Camera URL </label>
                            <input
                                v-model="ipCameraUrl"
                                type="text"
                                :disabled="isDetecting"
                                placeholder="contoh: http://192.168.1.194:8081/video"
                            />
                            <p class="setting-help">
                                Ambil URL ini dari aplikasi IP Camera di iPhone
                                setelah menekan tombol
                                <strong>Start Server</strong>.
                            </p>
                        </div>

                        <div class="stats-grid">
                            <div class="stat-box">
                                <div class="stat-label-small">Mode</div>
                                <div class="stat-value-small">
                                    {{ isDetecting ? "Live" : "Demo" }}
                                </div>
                            </div>
                            <div class="stat-box">
                                <div class="stat-label-small">Session ID</div>
                                <div class="stat-value-small">
                                    {{
                                        sessionId
                                            ? sessionId.substring(0, 8) + "..."
                                            : "N/A"
                                    }}
                                </div>
                            </div>
                        </div>
                    </div>

                    <div class="scenarios-panel">
                        <h3 class="scenarios-title">Detection Scenarios</h3>
                        <div class="scenarios-list">
                            <div
                                v-for="(scenario, index) in demoScenarios"
                                :key="index"
                                class="scenario-card animate-on-scroll"
                            >
                                <h4 class="scenario-title">
                                    {{ scenario.title }}
                                </h4>
                                <p class="scenario-description">
                                    {{ scenario.description }}
                                </p>
                                <div class="scenario-footer">
                                    <span class="scenario-badge">{{
                                        scenario.downloads
                                    }}</span>
                                    <span
                                        class="scenario-badge confidence-badge"
                                        >{{ scenario.complexity }}</span
                                    >
                                </div>
                            </div>
                        </div>
                    </div>


                </div>
            </div>
        </section>
    </div>
</template>

<style scoped>
.demo-fire-container {
    min-height: 100vh;
    background: #0f0f1e;
    padding: 80px 0;
}
.container {
    max-width: 1400px;
    margin: 0 auto;
    padding: 0 20px;
}
.action-section {
    margin-bottom: 80px;
}
.section-title {
    font-size: 3rem;
    font-weight: 800;
    color: #ffffff;
    text-align: center;
    margin-bottom: 16px;
}
.section-subtitle {
    font-size: 1.25rem;
    color: #fbbf24;
    text-align: center;
    margin-bottom: 60px;
}
.error-banner {
    background: rgba(239, 68, 68, 0.1);
    border: 2px solid rgba(239, 68, 68, 0.3);
    color: #ef4444;
    padding: 16px 24px;
    border-radius: 12px;
    margin-bottom: 30px;
    display: flex;
    align-items: center;
    justify-content: space-between;
}
.error-close {
    background: none;
    border: none;
    color: #ef4444;
    font-size: 1.5rem;
    cursor: pointer;
    padding: 0 8px;
    opacity: 0.7;
    transition: opacity 0.2s;
}
.error-close:hover {
    opacity: 1;
    cursor: pointer;
}
.video-container {
    max-width: 1200px;
    margin: 0 auto;
}
.video-wrapper {
    position: relative;
    background: #1a1a2e;
    border-radius: 20px;
    overflow: hidden;
    box-shadow: 0 20px 60px rgba(0, 0, 0, 0.5);
}
.demo-image-wrapper {
    position: relative;
    width: 100%;
}
.demo-video {
    width: 100%;
    height: auto;
    display: block;
    background: #000;
}
.overlay-layer {
    position: absolute;
    inset: 0;
    pointer-events: none;
    z-index: 9;
}
.video-overlay {
    position: absolute;
    top: 24px;
    right: 24px;
    z-index: 10;
}
.overlay-badge {
    background: rgba(139, 92, 246, 0.9);
    backdrop-filter: blur(10px);
    padding: 10px 20px;
    border-radius: 30px;
    color: white;
    font-size: 0.875rem;
    font-weight: 600;
    display: flex;
    align-items: center;
    gap: 8px;
}
.badge-dot {
    width: 8px;
    height: 8px;
    background: white;
    border-radius: 50%;
    animation: pulse 2s infinite;
}
@keyframes pulse {
    0%,
    100% {
        opacity: 1;
        transform: scale(1);
    }
    50% {
        opacity: 0.6;
        transform: scale(0.9);
    }
}
.video-stats {
    position: absolute;
    bottom: 24px;
    left: 24px;
    right: 24px;
    display: flex;
    gap: 24px;
    background: rgba(26, 26, 46, 0.95);
    backdrop-filter: blur(10px);
    padding: 20px;
    border-radius: 16px;
}
.stat-item {
    flex: 1;
    text-align: center;
}
.stat-label {
    display: block;
    font-size: 0.875rem;
    color: #9ca3af;
    margin-bottom: 6px;
    text-transform: uppercase;
    letter-spacing: 1px;
}
.stat-value {
    display: block;
    font-size: 1.5rem;
    font-weight: 700;
    color: #8b5cf6;
}
.video-caption {
    margin-top: 24px;
    text-align: center;
    color: #9ca3af;
    font-size: 1rem;
}

.try-section {
    background: #1a1a2e;
    border-radius: 24px;
    padding: 60px 40px;
}
.demo-grid {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 40px;
    margin-top: 40px;
}
.settings-panel,
.scenarios-panel {
    background: #16182a;
    border-radius: 20px;
    padding: 32px;
}
.panel-header {
    display: flex;
    align-items: center;
    gap: 12px;
    margin-bottom: 32px;
    padding-bottom: 24px;
    border-bottom: 2px solid #1e293b;
}
.panel-icon {
    font-size: 1.75rem;
}
.panel-header h3 {
    font-size: 1.5rem;
    font-weight: 700;
    color: #fff;
    margin: 0;
}
.play-button {
    width: 100%;
    padding: 18px 32px;
    background: linear-gradient(135deg, #8b5cf6 0%, #7c3aed 100%);
    color: #fff;
    border: none;
    border-radius: 12px;
    font-size: 1.1rem;
    font-weight: 600;
    cursor: pointer;
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 12px;
    transition: all 0.3s ease;
    margin-bottom: 32px;
}
.play-button:hover {
    transform: translateY(-2px);
    box-shadow: 0 12px 40px rgba(139, 92, 246, 0.4);
}
.stop-button {
    background: linear-gradient(135deg, #6b7280 0%, #4b5563 100%);
}
.button-icon {
    font-size: 1.25rem;
}
.setting-group {
    margin-bottom: 28px;
}
.setting-row {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 10px;
}
.setting-label {
    display: block;
    font-size: 1rem;
    font-weight: 600;
    color: #e5e7eb;
    margin-bottom: 12px;
}
.setting-value {
    color: #8b5cf6;
    margin-left: 8px;
}
.slider {
    width: 100%;
    height: 8px;
    border-radius: 4px;
    background: #1e293b;
    outline: none;
    -webkit-appearance: none;
    appearance: none;
}
.slider::-webkit-slider-thumb {
    -webkit-appearance: none;
    width: 20px;
    height: 20px;
    border-radius: 50%;
    background: linear-gradient(135deg, #8b5cf6 0%, #7c3aed 100%);
    cursor: pointer;
    box-shadow: 0 2px 10px rgba(139, 92, 246, 0.5);
}
.slider::-moz-range-thumb {
    width: 20px;
    height: 20px;
    border-radius: 50%;
    background: linear-gradient(135deg, #8b5cf6 0%, #7c3aed 100%);
    cursor: pointer;
    box-shadow: 0 2px 10px rgba(139, 92, 246, 0.5);
    border: none;
}
.slider:disabled {
    opacity: 0.5;
    cursor: not-allowed;
}
.setting-help {
    font-size: 0.875rem;
    color: #6b7280;
    margin-top: 8px;
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
    background: linear-gradient(135deg, #8b5cf6 0%, #7c3aed 100%);
}
.toggle-input:checked + .toggle-label:before {
    background-color: #fff;
    transform: translateX(24px);
}
.toggle-input:disabled + .toggle-label {
    opacity: 0.5;
    cursor: not-allowed;
}
.stats-grid {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 16px;
    margin-top: 32px;
    padding-top: 24px;
    border-top: 2px solid #1e293b;
}
.stat-box {
    background: #1e293b;
    padding: 16px;
    border-radius: 12px;
    text-align: center;
}
.stat-label-small {
    font-size: 0.75rem;
    color: #6b7280;
    text-transform: uppercase;
    letter-spacing: 1px;
    margin-bottom: 6px;
}
.stat-value-small {
    font-size: 1.125rem;
    font-weight: 600;
    color: #fff;
}
.scenarios-title {
    font-size: 1.5rem;
    font-weight: 700;
    color: #fff;
    margin-bottom: 24px;
}
.scenarios-list {
    display: flex;
    flex-direction: column;
    gap: 16px;
}
.scenario-card {
    background: #1e293b;
    border-radius: 12px;
    padding: 20px;
    transition: all 0.3s ease;
    cursor: pointer;
}
.scenario-card:hover {
    transform: translateY(-2px);
    box-shadow: 0 8px 24px rgba(139, 92, 246, 0.2);
}
.scenario-title {
    font-size: 1.125rem;
    font-weight: 600;
    color: #fff;
    margin-bottom: 10px;
}
.scenario-description {
    font-size: 0.875rem;
    color: #9ca3af;
    margin-bottom: 14px;
    line-height: 1.6;
}
.scenario-footer {
    display: flex;
    gap: 10px;
    flex-wrap: wrap;
}
.scenario-badge {
    font-size: 0.75rem;
    padding: 6px 14px;
    background: rgba(139, 92, 246, 0.1);
    color: #8b5cf6;
    border-radius: 20px;
    font-weight: 500;
}
.confidence-badge {
    background: rgba(251, 191, 36, 0.1);
    color: #fbbf24;
}
.custom-select {
    width: 100%;
    padding: 10px 14px;
    background: #1e293b;
    border: 1px solid #2d3748;
    color: #fff;
    border-radius: 8px;
    margin-bottom: 24px;
    outline: none;
    cursor: pointer;
}
.custom-select:focus {
    border-color: #8b5cf6;
}
.save-btn {
    width: 100%;
    padding: 14px;
    background: #1f2937;
    color: #fff;
    font-weight: 600;
    border-color: 1px solid #374151;
    border: none;
    border-radius: 8px;
    cursor: pointer;
    transition: all 0.3s;
    margin-top: 24px;
    text-transform: uppercase;
    letter-spacing: 0.5px;
}
.save-btn:hover {
    background: #374151;
}
@media (max-width: 968px) {
    .demo-grid {
        grid-template-columns: 1fr;
    }
    .section-title {
        font-size: 2rem;
    }
}

.loading-overlay {
    position: absolute;
    inset: 0;
    background: rgba(0, 0, 0, 0.8);
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    color: white;
    z-index: 10;
}
.loading-spinner {
    width: 50px;
    height: 50px;
    border: 4px solid rgba(139, 92, 246, 0.3);
    border-top-color: #8b5cf6;
    border-radius: 50%;
    animation: spin 1s linear infinite;
}
@keyframes spin {
    to {
        transform: rotate(360deg);
    }
}
.loading-overlay p {
    margin-top: 20px;
    font-size: 1.1rem;
    color: #8b5cf6;
}

.fire-detection-box {
    position: absolute;
    border: 4px solid #ff0000;
    border-radius: 4px;
    background: rgba(255, 0, 0, 0.08);
    pointer-events: none;
    z-index: 10;
    animation: fadeInOut 1.8s ease-in-out infinite;
}
.fire-detection-box.glow {
    border-color: #ff1a1a;
    animation: fadeInOut 1.8s ease-in-out infinite,
        pulseGlow 1.8s ease-in-out infinite;
}
.fire-label {
    position: absolute;
    top: -40px;
    left: 0;
    background: rgba(255, 0, 0, 0.95);
    color: #fff;
    padding: 10px 18px;
    border-radius: 8px;
    font-size: 15px;
    font-weight: 700;
    white-space: nowrap;
    animation: fadeInOut 1.8s ease-in-out infinite;
    box-shadow: 0 6px 16px rgba(255, 0, 0, 0.5);
    letter-spacing: 0.3px;
}
@keyframes fadeInOut {
    0%,
    100% {
        opacity: 0.4;
        transform: scale(0.98);
    }
    50% {
        opacity: 1;
        transform: scale(1);
    }
}
@keyframes pulseGlow {
    0%,
    100% {
        box-shadow: 0 0 15px rgba(255, 0, 0, 0.6), 0 0 30px rgba(255, 0, 0, 0.4),
            inset 0 0 15px rgba(255, 0, 0, 0.25);
    }
    50% {
        box-shadow: 0 0 25px rgba(255, 0, 0, 0.9), 0 0 50px rgba(255, 0, 0, 0.6),
            inset 0 0 20px rgba(255, 0, 0, 0.4);
    }
}
@media (max-width: 768px) {
    .fire-detection-box {
        border-width: 3px;
    }
    .fire-label {
        font-size: 13px;
        padding: 8px 14px;
        top: -35px;
    }
}

.camera-source-label {
    color: white !important;
}
.camera-source-help {
    color: white !important;
}

select {
    color: white;
    background: #1e293b;
    border: 1px solid #4b5563;
}

input[type="text"] {
    color: white;
    background: #1e293b;
    border: 1px solid #4b5563;
}

input[type="text"]::placeholder {
    color: #9ca3af;
}

/* Animation Classes */
.animate-on-scroll {
    opacity: 1;
    transform: translateY(0);
    transition: opacity 0.8s ease-out, transform 0.8s ease-out;
}

.animate-on-scroll.prepare-animate {
    opacity: 0;
    transform: translateY(30px);
}

.animate-on-scroll.animate {
    opacity: 1;
    transform: translateY(0);
}
</style>
