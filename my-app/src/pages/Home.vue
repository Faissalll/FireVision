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
});
</script>

<template>
    <div class="overflow-x-hidden">
        <div
            class="min-h-screen bg-[#4D41C0] flex items-center justify-center px-4"
            :class="{ 'animate-fadeInUp': firstVisit }"
        >
            <div class="max-w-4xl mx-auto text-center">
                <div class="mb-8 flex justify-center">
                    <div
                        class="w-32 h-32 bg-[#5D51D0] rounded-full flex items-center justify-center shadow-2xl"
                    >
                        <img
                            src="../assets/LogoWeb.png"
                            alt="FireVision Logo"
                            class="w-20 h-20 object-contain"
                        />
                    </div>
                </div>

                <h1 class="text-5xl md:text-6xl font-bold text-white mb-6">
                    FireVision – AI Fire & Smoke Detection
                </h1>

                <p class="text-xl md:text-2xl text-gray-200 mb-12">
                    Real-time fire and smoke monitoring powered by artificial
                    intelligence.
                </p>

                <div
                    class="flex flex-col sm:flex-row items-center justify-center gap-4"
                >
                    <button
                        class="bg-[#3D31B0] text-white px-8 py-3 rounded-lg font-semibold transition-all duration-500 ease-out shadow-lg hover:shadow-2xl hover:shadow-[#3D31B0]/60 flex items-center gap-2 hover:scale-105 hover:translate-z-10 perspective-1000 group"
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
                            >Try Demo</span
                        >
                    </button>

                    <button
                        class="bg-white text-gray-800 px-8 py-3 rounded-lg font-semibold transition-all duration-300 shadow-lg hover:shadow-2xl hover:shadow-white/30 hover:scale-[1.02] hover:-translate-y-1 group"
                    >
                        <span
                            class="group-hover:tracking-wide transition-all duration-300"
                            >Get Started</span
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

        <FeaturesSection />

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
</style>
