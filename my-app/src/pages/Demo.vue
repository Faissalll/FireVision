<script setup>
import DemoFire from "../components/DemoFire.vue";
import MultiCameraView from "../components/MultiCameraView.vue";
import Footer from "../components/Footer.vue";
import { onMounted, ref } from 'vue';

import Modal from "../components/Modal.vue";

const pageRef = ref(null);
const cameraMode = ref('single'); // 'single', 'multi2', 'multi4'

// Modal State
const showModal = ref(false);
const modalTitle = ref("");
const modalMessage = ref("");


const handleModeChange = (mode) => {
    if (mode === 'multi4') {
        const userStr = localStorage.getItem("user");
        const user = userStr ? JSON.parse(userStr) : {};
        if (user.plan !== 'premium' && user.username !== 'admin') { 
            // Simple check, assumming 'admin' or explicit 'premium' plan
            // Since default is 'free', strictly check for free
            if (!user.plan || user.plan === 'free') {
                modalTitle.value = "Fitur Premium";
                modalMessage.value = "Fitur Multi-Camera (4x) khusus untuk pengguna Premium. Silakan upgrade plan Anda untuk akses penuh!";
                showModal.value = true;
                return;
            }
        }
    }
    cameraMode.value = mode;
};

onMounted(() => {
    if (!pageRef.value) return;

    const elements = pageRef.value.querySelectorAll('.animate-on-scroll');
    const observer = new IntersectionObserver((entries) => {
        entries.forEach((entry) => {
            if (entry.isIntersecting) {
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
    <div ref="pageRef" class="demo-page">
        <div class="demo-header">
            <h1 class="demo-title animate-on-scroll">Demo Interaktif</h1>
            <p class="demo-subtitle animate-on-scroll">
                Rasakan deteksi api bertenaga AI dari FireVision secara langsung.
                Sesuaikan pengaturan dan lihat hasil secara real-time.
            </p>
            
            <div class="mode-switch animate-on-scroll">
                 <button 
                    class="switch-btn" 
                    :class="{ active: cameraMode === 'single' }"
                    @click="handleModeChange('single')"
                >
                    Single Camera
                </button>
                <button 
                    class="switch-btn" 
                    :class="{ active: cameraMode === 'multi2' }"
                    @click="handleModeChange('multi2')"
                >
                    Multi-Camera (2x)
                </button>
                <button 
                    class="switch-btn" 
                    :class="{ active: cameraMode === 'multi4' }"
                    @click="handleModeChange('multi4')"
                >
                    Multi-Camera (4x)
                </button>
            </div>

            <!-- History & Settings Buttons -->
            <div class="flex flex-wrap justify-center gap-4 mt-8 animate-on-scroll">
                <button 
                    @click="$router.push('/history')"
                    class="flex items-center gap-3 px-6 py-2 bg-[#1a1a2e]/50 border border-[#2d2d48] hover:border-[#6C4DFF] hover:text-[#6C4DFF] text-gray-300 rounded-full font-semibold transition-all duration-300 group shadow-lg hover:shadow-[#6C4DFF]/20 text-sm"
                >
                    <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="group-hover:scale-110 transition-transform"><path d="M3 3v18h18"/><path d="M18 17V9"/><path d="M13 17V5"/><path d="M8 17v-3"/></svg>
                    Riwayat Deteksi
                </button>

                <button 
                    @click="$router.push('/notifications')"
                    class="flex items-center gap-3 px-6 py-2 bg-[#1a1a2e]/50 border border-[#2d2d48] hover:border-[#FBBF24] hover:text-[#FBBF24] text-gray-300 rounded-full font-semibold transition-all duration-300 group shadow-lg hover:shadow-[#FBBF24]/20 text-sm"
                >
                    <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="group-hover:scale-110 transition-transform"><path d="M18 8A6 6 0 0 0 6 8c0 7-3 9-3 9h18s-3-2-3-9"/><path d="M13.73 21a2 2 0 0 1-3.46 0"/></svg>
                    Atur Notifikasi
                </button>
            </div>
        </div>

        <div v-if="cameraMode === 'single'">
            <DemoFire />
        </div>
        <div v-else>
            <MultiCameraView :maxCameras="cameraMode === 'multi4' ? 4 : 2" />
        </div>



        <Footer />
        
        <!-- Custom Modal -->
        <Modal 
            :isOpen="showModal" 
            :title="modalTitle" 
            :message="modalMessage" 
            @close="showModal = false" 
        />
    </div>
</template>

<style scoped>
.demo-page {
    min-height: 100vh;
    background-color: #0f0f1e;
}

.demo-header {
    background: linear-gradient(180deg, #1a1a2e 0%, #0f0f1e 100%);
    padding: 80px 20px 60px;
    text-align: center;
}

.demo-title {
    font-size: 3.5rem;
    font-weight: 700;
    color: #ffffff;
    margin: 0 0 24px 0;
    letter-spacing: -0.5px;
}

.demo-subtitle {
    font-size: 1.25rem;
    color: #b0b0c3;
    max-width: 800px;
    margin: 0 auto;
    line-height: 1.6;
}

.mode-switch {
    display: flex;
    justify-content: center;
    gap: 15px;
    margin-top: 30px;
}

.switch-btn {
    padding: 10px 24px;
    border-radius: 30px;
    border: 2px solid #2d2d48;
    background: transparent;
    color: #b0b0c3;
    font-weight: 600;
    cursor: pointer;
    transition: all 0.3s ease;
}

.switch-btn.active {
    background: #8b5cf6;
    border-color: #8b5cf6;
    color: white;
    box-shadow: 0 0 15px rgba(139, 92, 246, 0.4);
}

.switch-btn:hover:not(.active) {
    border-color: #8b5cf6;
    color: white;
}


@keyframes fadeInOut {
    0%, 100% {
        opacity: 0;
        transform: scale(0.95);
    }
    50% {
        opacity: 1;
        transform: scale(1);
    }
}

@keyframes pulse {
    0%, 100% {
        box-shadow: 0 0 0 0 rgba(255, 0, 0, 0.7);
    }
    50% {
        box-shadow: 0 0 0 15px rgba(255, 0, 0, 0);
    }
}

:deep(.fire-detection-box) {
    position: absolute;
    border: 3px solid #ff0000;
    border-radius: 8px;
    animation: fadeInOut 2s ease-in-out infinite, pulse 2s ease-in-out infinite;
    pointer-events: none;
    z-index: 10;
}


:deep(.fire-detection-box.glow) {
    border: 3px solid #ff3333;
    box-shadow: 
        0 0 10px rgba(255, 0, 0, 0.5),
        0 0 20px rgba(255, 0, 0, 0.3),
        inset 0 0 10px rgba(255, 0, 0, 0.2);
}


:deep(.fire-label) {
    position: absolute;
    top: -30px;
    left: 0;
    background: rgba(255, 0, 0, 0.9);
    color: white;
    padding: 5px 12px;
    border-radius: 4px;
    font-size: 14px;
    font-weight: 600;
    animation: fadeInOut 2s ease-in-out infinite;
}



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

@media (max-width: 768px) {
    .demo-title {
        font-size: 2.5rem;
    }

    .demo-subtitle {
        font-size: 1rem;
    }

    .demo-header {
        padding: 60px 20px 40px;
    }
    
    :deep(.fire-detection-box) {
        border-width: 2px;
    }
    
    :deep(.fire-label) {
        font-size: 12px;
        padding: 4px 10px;
    }
}
</style>
