<script setup>
import { ref, onMounted } from "vue";
import FeaturesSection from "../components/FeaturesSection.vue";
import HowItWorksSection from "../components/HowItWorksSection.vue";
import TrustedAcrossIndustries from "../components/TrustedAcrossIndustries.vue";
import ProtectEnvironment from "../components/ProtectEnvironment.vue";
import Footer from "../components/Footer.vue";
import ResedentialBg from "../assets/resedential.jpg"; // Import background image

const firstVisit = ref(false);

onMounted(() => {
    if (!localStorage.getItem("visitedHome")) {
        firstVisit.value = true;
        localStorage.setItem("visitedHome", "true");
    }

    const observer = new IntersectionObserver((entries) => {
        entries.forEach((entry) => {
            if (entry.isIntersecting) {
                entry.target.classList.remove('prepare-animate');
                entry.target.classList.add('animate');
                observer.unobserve(entry.target);
            }
        });
    }, { threshold: 0.1 });

    document.querySelectorAll('.animate-hero').forEach((el, index) => {
        el.style.transitionDelay = `${index * 0.1}s`;
        el.classList.add('prepare-animate');
        observer.observe(el);
    });
});
</script>

<template>
    <div class="overflow-x-hidden bg-[#0f0f1a]">
        
        <!-- NEW HERO SECTION BASED ON TSX + USER REQUEST -->
        <section class="relative min-h-screen flex items-center justify-center overflow-hidden">
            
            <!-- Background Image with Overlay -->
            <div class="absolute inset-0 z-0">
                <img 
                    :src="ResedentialBg" 
                    alt="Fire Detection" 
                    class="w-full h-full object-cover opacity-40 transition-transform duration-1000 hover:scale-105" 
                />
                <div class="absolute inset-0 bg-gradient-to-b from-[#0f0f1a]/95 via-[#0f0f1a]/80 to-[#0f0f1a]"></div>
            </div>

            <!-- Animated Gradient Orbs -->
            <div class="absolute top-20 left-10 w-96 h-96 bg-[#5d51e8] rounded-full blur-[120px] opacity-20 animate-pulse hidden md:block"></div>
            <div class="absolute bottom-20 right-10 w-96 h-96 bg-[#ff4d4d] rounded-full blur-[120px] opacity-10 animate-pulse hidden md:block" style="animation-delay: 1s;"></div>

            <!-- Content -->
            <div class="relative z-10 container mx-auto px-6 py-20 mt-10">
                <div class="max-w-5xl mx-auto text-center">
                    
                    <!-- Logo/Icon with Glow -->
                    <div class="mb-8 flex justify-center animate-hero">
                        <div class="relative group">
                            <div class="absolute -inset-1 bg-[#5d51e8] rounded-full blur-xl opacity-75 group-hover:opacity-100 transition duration-1000 group-hover:duration-200"></div>
                            <div class="relative w-24 h-24 bg-[#1a1a2e] rounded-full flex items-center justify-center border border-[#5d51e8]/50 shadow-[0_0_40px_rgba(93,81,232,0.6)]">
                                <img src="../assets/LOGO.svg" alt="FireVision Logo" class="w-12 h-12 object-contain drop-shadow-[0_0_15px_rgba(93,81,232,0.9)]" />
                            </div>
                        </div>
                    </div>

                    <!-- Headline -->
                    <h1 class="mb-6 bg-gradient-to-r from-white via-white to-[#cfcfcf] bg-clip-text text-transparent font-bold leading-tight animate-hero title-responsive">
                        FireVision – Deteksi Api AI
                    </h1>

                    <!-- Subheadline -->
                    <p class="mb-10 text-[#cfcfcf] max-w-3xl mx-auto text-xl md:text-2xl leading-relaxed font-light animate-hero">
                        Pemantauan api real-time yang didukung oleh kecerdasan buatan.
                    </p>

                    <!-- CTA Buttons -->
                    <div class="flex flex-wrap gap-6 justify-center mb-12 animate-hero">
                        <button 
                            @click="$router.push('/demo')"
                            class="flex items-center gap-3 px-8 py-4 bg-[#5d51e8] hover:bg-[#4a3eb8] text-white rounded-lg font-semibold text-lg shadow-lg shadow-[#5d51e8]/50 transition-all hover:shadow-xl hover:shadow-[#5d51e8]/60 hover:scale-105"
                        >
                            <!-- Video Icon -->
                            <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                                <path d="m22 8-6 4 6 4V8Z"/><rect width="14" height="12" x="2" y="6" rx="2" ry="2"/>
                            </svg>
                            Coba Demo
                        </button>
                        
                        <button 
                            @click="$router.push('/features')"
                            class="px-8 py-4 bg-transparent border-2 border-[#5d51e8] text-white hover:bg-[#5d51e8]/10 rounded-lg font-semibold text-lg backdrop-blur-sm transition-all hover:scale-105"
                        >
                            Mulai Sekarang
                        </button>
                    </div>

                </div>
            </div>

            <!-- Scroll Indicator -->
            <div class="absolute bottom-8 left-1/2 transform -translate-x-1/2 z-10 animate-bounce">
                <div class="w-6 h-10 border-2 border-[#5d51e8] rounded-full flex justify-center pt-2">
                    <div class="w-1 h-2 bg-[#5d51e8] rounded-full"></div>
                </div>
            </div>
        </section>

        <FeaturesSection titlePosition="top" />

        <HowItWorksSection />

        <TrustedAcrossIndustries />

        <ProtectEnvironment />

        <Footer />
    </div>
</template>

<style scoped>
* {
    max-width: 100%;
}

.title-responsive {
    font-size: 2.5rem;
}
@media (min-width: 768px) {
    .title-responsive {
        font-size: 4rem;
    }
}

.animate-hero {
    opacity: 1;
    transform: translateY(0);
    transition: opacity 0.8s ease-out, transform 0.8s ease-out;
}

.animate-hero.prepare-animate {
    opacity: 0;
    transform: translateY(30px);
}

.animate-hero.animate {
    opacity: 1;
    transform: translateY(0);
}
</style>
