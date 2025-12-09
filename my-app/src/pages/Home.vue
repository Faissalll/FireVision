<script setup>
import { ref, onMounted } from "vue";
import FeaturesSection from "../components/FeaturesSection.vue";
import HowItWorksSection from "../components/HowItWorksSection.vue";
import TrustedAcrossIndustries from "../components/TrustedAcrossIndustries.vue";
import ProtectEnvironment from "../components/ProtectEnvironment.vue";
import Footer from "../components/Footer.vue";

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
    <div class="overflow-x-hidden">
        <div
            class="min-h-screen bg-[#4D41C0] flex items-center justify-center px-4"
        >
            <div class="max-w-4xl mx-auto text-center">
                <div class="mb-8 flex justify-center animate-hero">
                    <div
                        class="w-64 h-64 bg-[#5D51D0] rounded-full flex items-center justify-center shadow-2xl"
                    >
                        <img
                            src="../assets/LOGO.svg"
                            alt="FireVision Logo"
                            class="w-40 h-40 object-contain"
                        />
                    </div>
                </div>

                <h1 class="text-5xl md:text-6xl font-bold text-white mb-6 animate-hero">
                    FireVision – Deteksi Api & Asap AI
                </h1>

                <p class="text-xl md:text-2xl text-gray-200 mb-12 animate-hero">
                    Pemantauan api dan asap real-time yang didukung oleh kecerdasan buatan.
                </p>

                <div
                    class="flex flex-col sm:flex-row items-center justify-center gap-4 animate-hero"
                >
                    <button
                         @click="$router.push('/demo')"
                        class="bg-[#3D31B0] text-white px-8 py-3 rounded-lg font-semibold transition-all duration-300 shadow-lg hover:shadow-2xl hover:shadow-[#3D31B0]/60 flex items-center gap-2 hover:scale-105 group"
                    >
                        <svg
                            class="w-5 h-5 group-hover:animate-pulse"
                            fill="currentColor"
                            viewBox="0 0 20 20"
                        >
                            <path d="M10 12a2 2 0 100-4 2 2 0 000 4z" />
                            <path
                                fill-rule="evenodd"
                                d="M.458 10C1.732 5.943 5.522 3 10 3s8.268 2.943 9.542 7c-1.274 4.057-5.064 7-9.542 7S1.732 14.057.458 10zM14 10a4 4 0 11-8 0 4 4 0 018 0z"
                                clip-rule="evenodd"
                            />
                        </svg>
                        <span
                            class="group-hover:tracking-wide transition-all duration-300"
                            >Coba Demo</span
                        >
                    </button>

                    <button
                        @click="$router.push('/features')"
                        class="bg-white text-gray-800 px-8 py-3 rounded-lg font-semibold transition-all duration-300 shadow-lg hover:shadow-2xl hover:shadow-white/30 hover:scale-[1.02] hover:-translate-y-1 group"
                    >
                        <span
                            class="group-hover:tracking-wide transition-all duration-300"
                            >Mulai Sekarang</span
                        >
                        <svg
                            class="w-5 h-5 inline-block ml-2 group-hover:translate-x-1 transition-transform duration-300"
                            fill="none"
                            stroke="currentColor"
                            viewBox="0 0 24 24"
                        >
                            <path
                                stroke-linecap="round"
                                stroke-linejoin="round"
                                stroke-width="2"
                                d="M13 7l5 5m0 0l-5 5m5-5H6"
                            />
                        </svg>
                    </button>
                </div>
            </div>
        </div>

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

.perspective-1000 {
    perspective: 1000px;
}

.hover\:translate-z-10:hover {
    transform: translateZ(10px);
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
