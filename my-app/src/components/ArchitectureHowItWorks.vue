<template>
    <section ref="sectionRef" class="technical-architecture">
        <div class="container">
            <h2 class="section-title">Arsitektur Teknis</h2>
            <p class="section-subtitle">
                Dibangun di atas infrastruktur tingkat perusahaan dengan teknologi AI
                mutakhir
            </p>

            <div class="architecture-grid">
                <div class="architecture-card">
                    <div class="card-header">
                        <div class="card-icon video-icon">
                            <svg
                                xmlns="http://www.w3.org/2000/svg"
                                width="24"
                                height="24"
                                viewBox="0 0 24 24"
                                fill="none"
                                stroke="currentColor"
                                stroke-width="2"
                                stroke-linecap="round"
                                stroke-linejoin="round"
                            >
                                <polygon
                                    points="23 7 16 12 23 17 23 7"
                                ></polygon>
                                <rect
                                    x="1"
                                    y="5"
                                    width="15"
                                    height="14"
                                    rx="2"
                                    ry="2"
                                ></rect>
                            </svg>
                        </div>
                        <h3 class="card-title">Input & Pemrosesan Video</h3>
                    </div>
                    <p class="card-description">
                        FireVision mendukung berbagai protokol dan format kamera,
                        memproses aliran video hingga resolusi 4K dengan latensi minimal.
                    </p>
                    <ul class="feature-list">
                        <li>Protokol ONVIF, RTSP, HTTP</li>
                        <li>Dukungan resolusi hingga 4K</li>
                        <li>Dukungan codec H.264, H.265</li>
                        <li>Pemrosesan 30+ FPS</li>
                    </ul>
                </div>
                <div class="architecture-card">
                    <div class="card-header">
                        <div class="card-icon ai-icon">
                            <svg
                                xmlns="http://www.w3.org/2000/svg"
                                width="24"
                                height="24"
                                viewBox="0 0 24 24"
                                fill="none"
                                stroke="currentColor"
                                stroke-width="2"
                                stroke-linecap="round"
                                stroke-linejoin="round"
                            >
                                <circle cx="12" cy="12" r="10"></circle>
                                <line x1="12" y1="8" x2="12" y2="12"></line>
                                <line x1="12" y1="16" x2="12.01" y2="16"></line>
                            </svg>
                        </div>
                        <h3 class="card-title">Mesin Deteksi AI</h3>
                    </div>
                    <p class="card-description">
                        Model deep learning kami menggunakan convolutional neural networks
                        yang dilatih pada jutaan skenario api dan asap.
                    </p>
                    <ul class="feature-list">
                        <li>Arsitektur YOLOv8</li>
                        <li>Model terlatih khusus</li>
                        <li>Inferensi real-time</li>
                        <li>Pembelajaran berkelanjutan</li>
                    </ul>
                </div>
                <div class="architecture-card">
                    <div class="card-header">
                        <div class="card-icon edge-icon">
                            <svg
                                xmlns="http://www.w3.org/2000/svg"
                                width="24"
                                height="24"
                                viewBox="0 0 24 24"
                                fill="none"
                                stroke="currentColor"
                                stroke-width="2"
                                stroke-linecap="round"
                                stroke-linejoin="round"
                            >
                                <rect
                                    x="2"
                                    y="3"
                                    width="20"
                                    height="14"
                                    rx="2"
                                    ry="2"
                                ></rect>
                                <line x1="8" y1="21" x2="16" y2="21"></line>
                                <line x1="12" y1="17" x2="12" y2="21"></line>
                            </svg>
                        </div>
                        <h3 class="card-title">Komputasi Edge</h3>
                    </div>
                    <p class="card-description">
                        Terapkan pemrosesan AI di edge untuk mengurangi latency dan
                        meningkatkan privasi, atau gunakan pemrosesan cloud untuk skalabilitas.
                    </p>
                    <ul class="feature-list">
                        <li>NVIDIA Jetson support</li>
                        <li>Intel Movidius VPU</li>
                        <li>ARM-based processors</li>
                        <li>GPU acceleration</li>
                    </ul>
                </div>

                <div class="architecture-card">
                    <div class="card-header">
                        <div class="card-icon alert-icon">
                            <svg
                                xmlns="http://www.w3.org/2000/svg"
                                width="24"
                                height="24"
                                viewBox="0 0 24 24"
                                fill="none"
                                stroke="currentColor"
                                stroke-width="2"
                                stroke-linecap="round"
                                stroke-linejoin="round"
                            >
                                <path
                                    d="M22 17H2a3 3 0 0 0 3-3V9a7 7 0 0 1 14 0v5a3 3 0 0 0 3 3zm-8.27 4a2 2 0 0 1-3.46 0"
                                ></path>
                            </svg>
                        </div>
                        <h3 class="card-title">Sistem Peringatan</h3>
                    </div>
                    <p class="card-description">
                        Sistem notifikasi multi-saluran dengan aturan yang dapat disesuaikan
                        dan alur kerja eskalasi untuk situasi kritis.
                    </p>
                    <ul class="feature-list">
                        <li>SMS, Email, Notifikasi Push</li>
                        <li>Integrasi Webhook</li>
                        <li>Alur kerja eskalasi</li>
                        <li>Routing berbasis prioritas</li>
                    </ul>
                </div>
            </div>
        </div>
    </section>
</template>

<script setup>
import { onMounted, ref } from 'vue';

const sectionRef = ref(null);

onMounted(() => {
    if (!sectionRef.value) return;

    // Use scoped querySelectorAll for reliability
    const cards = sectionRef.value.querySelectorAll('.architecture-card');
    
    const observer = new IntersectionObserver((entries) => {
        entries.forEach((entry, index) => {
            if (entry.isIntersecting) {
                // Add stagger effect
                entry.target.style.transitionDelay = `${index * 0.15}s`;
                entry.target.classList.remove('prepare-animate');
                entry.target.classList.add('animate');
                observer.unobserve(entry.target);
            }
        });
    }, {
        threshold: 0.1
    });

    cards.forEach(card => {
        card.classList.add('prepare-animate');
        observer.observe(card);
    });
});
</script>

<style scoped>
.technical-architecture {
    padding: 80px 20px;
    background: #0f0f1e;
    color: #ffffff;
    min-height: 100vh;
    position: relative;
    overflow: hidden;
}


.container {
    max-width: 1200px;
    margin: 0 auto;
    position: relative;
    z-index: 1;
}

.section-title {
    font-size: 2.5rem;
    font-weight: 700;
    text-align: center;
    margin-bottom: 16px;
    color: #ffffff;
}

.section-subtitle {
    text-align: center;
    color: #a0a0a0;
    font-size: 1rem;
    margin-bottom: 60px;
    font-weight: 300;
}

.architecture-grid {
    display: grid;
    grid-template-columns: repeat(2, 1fr);
    gap: 24px;
    margin-top: 40px;
}

.architecture-card {
    background: rgba(30, 33, 48, 0.8);
    border: 1px solid rgba(255, 255, 255, 0.08);
    border-radius: 12px;
    padding: 32px;
    transition: all 0.6s ease-out;
    opacity: 1;
    transform: translateY(0);
}

.architecture-card.prepare-animate {
    opacity: 0;
    transform: translateY(30px);
}

.architecture-card.animate {
    opacity: 1;
    transform: translateY(0);
}

.architecture-card:hover {
    transform: translateY(-2px);
    border-color: #4d41c0;
    box-shadow: 0 0 30px rgba(77, 65, 192, 0.5);
}

.card-header {
    display: flex;
    align-items: center;
    gap: 16px;
    margin-bottom: 16px;
}

.card-icon {
    width: 48px;
    height: 48px;
    border-radius: 10px;
    display: flex;
    align-items: center;
    justify-content: center;
    flex-shrink: 0;
    color: white;
}

.video-icon {
    background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%);
}

.ai-icon {
    background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%);
}

.edge-icon {
    background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%);
}

.alert-icon {
    background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%);
}

.card-title {
    font-size: 1.25rem;
    font-weight: 600;
    margin: 0;
    color: #ffffff;
}

.card-description {
    color: #9ca3af;
    line-height: 1.6;
    margin-bottom: 20px;
    font-size: 0.95rem;
}

.feature-list {
    list-style: none;
    padding: 0;
    margin: 0;
}

.feature-list li {
    color: #d1d5db;
    padding: 6px 0;
    padding-left: 20px;
    position: relative;
    font-size: 0.9rem;
}

.feature-list li::before {
    content: "▸";
    position: absolute;
    left: 0;
    color: #6366f1;
    font-weight: bold;
}

@media (max-width: 768px) {
    .section-title {
        font-size: 2rem;
    }

    .architecture-grid {
        grid-template-columns: 1fr;
        gap: 20px;
    }

    .technical-architecture {
        padding: 60px 20px;
    }

    .card-header {
        flex-direction: column;
        align-items: flex-start;
    }
}
</style>
