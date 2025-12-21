<template>
    <div ref="sectionRef" class="bg-[#0F0F1E] py-20 px-4">
        <div class="max-w-7xl mx-auto">
            <div class="text-center mb-16">
                <h2 class="text-4xl md:text-5xl font-bold text-white mb-4">
                    Terpercaya di Berbagai Industri
                </h2>
                <p class="text-xl text-gray-400">
                    FireVision melindungi beragam sektor dengan solusi deteksi kebakaran yang disesuaikan
                </p>
            </div>

            <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
                <div
                    class="industry-card bg-[#1A1A2E] rounded-2xl overflow-hidden border border-[#33333C] hover:border-[#4D41C0] hover:shadow-[0_0_30px_rgba(77,65,192,0.5)] transition-all duration-300"
                >
                    <div
                        class="relative h-64 bg-gradient-to-b from-gray-700 to-gray-900"
                    >
                        <img
                            src="../assets/industrial_v2.jpg"
                            alt="Industrial Facilities"
                            class="w-full h-full object-cover"
                        />

                        <div
                            class="absolute top-4 right-4 w-14 h-14 bg-[#4D41C0] rounded-full flex items-center justify-center shadow-lg"
                        >
                            <svg
                                class="w-7 h-7 text-white"
                                fill="currentColor"
                                viewBox="0 0 24 24"
                            >
                                <path
                                    d="M18 10V4c0-.6-.4-1-1-1h-4c-.6 0-1 .4-1 1v2L8 3c-.6 0-1 .4-1 1v6H3v10c0 .6.4 1 1 1h16c.6 0 1-.4 1-1V10h-3zm-8-6h2v2h-2V4zM5 19v-7h14v7H5z"
                                />
                                <rect x="7" y="13" width="2" height="2" />
                                <rect x="11" y="13" width="2" height="2" />
                                <rect x="15" y="13" width="2" height="2" />
                                <rect x="7" y="16" width="2" height="2" />
                                <rect x="11" y="16" width="2" height="2" />
                                <rect x="15" y="16" width="2" height="2" />
                            </svg>
                        </div>
                    </div>

                    <div class="p-8">
                        <h3 class="text-2xl font-bold text-white mb-4">
                            Fasilitas Industri
                        </h3>
                        <p class="text-gray-400 mb-6 leading-relaxed">
                            Lindungi pabrik manufaktur, gudang, dan kompleks industri
                            dengan pemantauan AI 24/7.
                        </p>

                        <ul class="space-y-3">
                            <li class="flex items-center gap-3 text-gray-300">
                                <svg
                                    class="w-5 h-5 text-[#4D41C0] flex-shrink-0"
                                    fill="currentColor"
                                    viewBox="0 0 20 20"
                                >
                                    <path
                                        fill-rule="evenodd"
                                        d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z"
                                        clip-rule="evenodd"
                                    />
                                </svg>
                                <span>Keamanan penyimpanan bahan kimia</span>
                            </li>
                            <li class="flex items-center gap-3 text-gray-300">
                                <svg
                                    class="w-5 h-5 text-[#4D41C0] flex-shrink-0"
                                    fill="currentColor"
                                    viewBox="0 0 20 20"
                                >
                                    <path
                                        fill-rule="evenodd"
                                        d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z"
                                        clip-rule="evenodd"
                                    />
                                </svg>
                                <span>Pemantauan peralatan</span>
                            </li>
                            <li class="flex items-center gap-3 text-gray-300">
                                <svg
                                    class="w-5 h-5 text-[#4D41C0] flex-shrink-0"
                                    fill="currentColor"
                                    viewBox="0 0 20 20"
                                >
                                    <path
                                        fill-rule="evenodd"
                                        d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z"
                                        clip-rule="evenodd"
                                    />
                                </svg>
                                <span>Perlindungan pekerja</span>
                            </li>
                        </ul>
                    </div>
                </div>

                <div
                    class="industry-card bg-[#1A1A2E] rounded-2xl overflow-hidden border border-[#33333C] hover:border-[#4D41C0] hover:shadow-[0_0_30px_rgba(77,65,192,0.5)] transition-all duration-300"
                >
                    <div
                        class="relative h-64 bg-gradient-to-b from-gray-700 to-gray-900"
                    >
                        <img
                            src="../assets/public-safety.jpg"
                            alt="Public Safety"
                            class="w-full h-full object-cover"
                        />

                        <div
                            class="absolute top-4 right-4 w-14 h-14 bg-[#4D41C0] rounded-full flex items-center justify-center shadow-lg"
                        >
                            <svg
                                class="w-7 h-7 text-white"
                                fill="none"
                                stroke="currentColor"
                                viewBox="0 0 24 24"
                            >
                                <path
                                    stroke-linecap="round"
                                    stroke-linejoin="round"
                                    stroke-width="2"
                                    d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5m-9 0H3m2 0h5M9 7h1m-1 4h1m4-4h1m-1 4h1m-5 10v-5a1 1 0 011-1h2a1 1 0 011 1v5m-4 0h4"
                                />
                            </svg>
                        </div>
                    </div>

                    <div class="p-8">
                        <h3 class="text-2xl font-bold text-white mb-4">
                            Keamanan Publik
                        </h3>
                        <p class="text-gray-400 mb-6 leading-relaxed">
                            Terapkan di bandara, mal, rumah sakit, dan tempat umum
                            untuk langkah-langkah keamanan yang ditingkatkan.
                        </p>

                        <ul class="space-y-3">
                            <li class="flex items-center gap-3 text-gray-300">
                                <svg
                                    class="w-5 h-5 text-[#4D41C0] flex-shrink-0"
                                    fill="currentColor"
                                    viewBox="0 0 20 20"
                                >
                                    <path
                                        fill-rule="evenodd"
                                        d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z"
                                        clip-rule="evenodd"
                                    />
                                </svg>
                                <span>Keamanan keramaian</span>
                            </li>
                            <li class="flex items-center gap-3 text-gray-300">
                                <svg
                                    class="w-5 h-5 text-[#4D41C0] flex-shrink-0"
                                    fill="currentColor"
                                    viewBox="0 0 20 20"
                                >
                                    <path
                                        fill-rule="evenodd"
                                        d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z"
                                        clip-rule="evenodd"
                                    />
                                </svg>
                                <span>Infrastruktur kritis</span>
                            </li>
                            <li class="flex items-center gap-3 text-gray-300">
                                <svg
                                    class="w-5 h-5 text-[#4D41C0] flex-shrink-0"
                                    fill="currentColor"
                                    viewBox="0 0 20 20"
                                >
                                    <path
                                        fill-rule="evenodd"
                                        d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z"
                                        clip-rule="evenodd"
                                    />
                                </svg>
                                <span>Respons darurat</span>
                            </li>
                        </ul>
                    </div>
                </div>

                <div
                    class="industry-card bg-[#1A1A2E] rounded-2xl overflow-hidden border border-[#33333C] hover:border-[#4D41C0] hover:shadow-[0_0_30px_rgba(77,65,192,0.5)] transition-all duration-300"
                >
                    <div
                        class="relative h-64 bg-gradient-to-b from-gray-700 to-gray-900"
                    >
                        <img
                            src="../assets/resedential.jpg"
                            alt="Residential"
                            class="w-full h-full object-cover"
                        />

                        <div
                            class="absolute top-4 right-4 w-14 h-14 bg-[#4D41C0] rounded-full flex items-center justify-center shadow-lg"
                        >
                            <svg
                                class="w-7 h-7 text-white"
                                fill="none"
                                stroke="currentColor"
                                viewBox="0 0 24 24"
                            >
                                <path
                                    stroke-linecap="round"
                                    stroke-linejoin="round"
                                    stroke-width="2"
                                    d="M3 12l2-2m0 0l7-7 7 7M5 10v10a1 1 0 001 1h3m10-11l2 2m-2-2v10a1 1 0 01-1 1h-3m-6 0a1 1 0 001-1v-4a1 1 0 011-1h2a1 1 0 011 1v4a1 1 0 001 1m-6 0h6"
                                />
                            </svg>
                        </div>
                    </div>

                    <div class="p-8">
                        <h3 class="text-2xl font-bold text-white mb-4">
                            Perumahan
                        </h3>
                        <p class="text-gray-400 mb-6 leading-relaxed">
                            Deteksi kebakaran cerdas untuk gedung apartemen,
                            kondominium, dan komunitas perumahan.
                        </p>

                        <ul class="space-y-3">
                            <li class="flex items-center gap-3 text-gray-300">
                                <svg
                                    class="w-5 h-5 text-[#4D41C0] flex-shrink-0"
                                    fill="currentColor"
                                    viewBox="0 0 20 20"
                                >
                                    <path
                                        fill-rule="evenodd"
                                        d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z"
                                        clip-rule="evenodd"
                                    />
                                </svg>
                                <span>Pemantauan rumah 24/7</span>
                            </li>
                            <li class="flex items-center gap-3 text-gray-300">
                                <svg
                                    class="w-5 h-5 text-[#4D41C0] flex-shrink-0"
                                    fill="currentColor"
                                    viewBox="0 0 20 20"
                                >
                                    <path
                                        fill-rule="evenodd"
                                        d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z"
                                        clip-rule="evenodd"
                                    />
                                </svg>
                                <span>Perlindungan keluarga</span>
                            </li>
                            <li class="flex items-center gap-3 text-gray-300">
                                <svg
                                    class="w-5 h-5 text-[#4D41C0] flex-shrink-0"
                                    fill="currentColor"
                                    viewBox="0 0 20 20"
                                >
                                    <path
                                        fill-rule="evenodd"
                                        d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z"
                                        clip-rule="evenodd"
                                    />
                                </svg>
                                <span>Integrasi rumah pintar</span>
                            </li>
                        </ul>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script setup>
import { onMounted, ref } from 'vue';

const sectionRef = ref(null);

onMounted(() => {
    if (!sectionRef.value) return;

    // Use scoped querySelectorAll for reliability
    const cards = sectionRef.value.querySelectorAll('.industry-card');
    
    const observer = new IntersectionObserver((entries) => {
        entries.forEach((entry, index) => {
            if (entry.isIntersecting) {
                // Add stagger effect
                entry.target.style.transitionDelay = `${index * 0.2}s`;
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
.industry-card {
    opacity: 1;
    transform: translateY(0);
    transition: all 0.6s ease-out;
}

.industry-card.prepare-animate {
    opacity: 0;
    transform: translateY(30px);
}

.industry-card.animate {
    opacity: 1;
    transform: translateY(0);
}
</style>
