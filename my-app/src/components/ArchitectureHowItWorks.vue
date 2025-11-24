<template>
    <section class="technical-architecture">
        <div class="container">
            <h2 class="section-title">Technical Architecture</h2>
            <p class="section-subtitle">
                Built on enterprise-grade infrastructure with cutting-edge AI
                technology
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
                        <h3 class="card-title">Video Input & Processing</h3>
                    </div>
                    <p class="card-description">
                        FireVision supports multiple camera protocols and
                        formats, processing video streams at up to 4K resolution
                        with minimal latency.
                    </p>
                    <ul class="feature-list">
                        <li>ONVIF, RTSP, HTTP protocols</li>
                        <li>Up to 4K resolution support</li>
                        <li>H.264, H.265 codec support</li>
                        <li>30+ FPS processing</li>
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
                        <h3 class="card-title">AI Detection Engine</h3>
                    </div>
                    <p class="card-description">
                        Our proprietary deep learning models use convolutional
                        neural networks trained on millions of fire and smoke
                        scenarios.
                    </p>
                    <ul class="feature-list">
                        <li>YOLOv8 architecture</li>
                        <li>Custom-trained models</li>
                        <li>Real-time inference</li>
                        <li>Continuous learning</li>
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
                        <h3 class="card-title">Edge Computing</h3>
                    </div>
                    <p class="card-description">
                        Deploy AI processing at the edge for reduced latency and
                        enhanced privacy, or use cloud processing for
                        scalability.
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
                        <h3 class="card-title">Alert System</h3>
                    </div>
                    <p class="card-description">
                        Multi-channel notification system with customizable
                        rules and escalation workflows for critical situations.
                    </p>
                    <ul class="feature-list">
                        <li>SMS, Email, Push notifications</li>
                        <li>Webhook integrations</li>
                        <li>Escalation workflows</li>
                        <li>Priority-based routing</li>
                    </ul>
                </div>
            </div>
        </div>
    </section>
</template>

<script>
export default {
    name: "TechnicalArchitecture",
};
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
    transition: all 0.3s ease;
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
