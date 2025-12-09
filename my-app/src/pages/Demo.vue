<script setup>
import DemoFire from "../components/DemoFire.vue";
import Footer from "../components/Footer.vue";
</script>

<template>
    <div class="demo-page">
        <div class="demo-header">
            <h1 class="demo-title">Demo Interaktif</h1>
            <p class="demo-subtitle">
                Rasakan deteksi api bertenaga AI dari FireVision secara langsung.
                Sesuaikan pengaturan dan lihat hasil secara real-time.
            </p>
        </div>

        <DemoFire />

        <Footer />
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
