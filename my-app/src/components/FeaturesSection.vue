<template>
  <div class="bg-[#0F0F1E] py-20 px-4">
    <div class="max-w-7xl mx-auto">

      <div class="text-center mb-16">
        <h2 class="text-4xl md:text-5xl font-bold text-white mb-4">
          Fitur Canggih
        </h2>
        <p class="text-xl text-gray-400">
          FireVision menggabungkan AI mutakhir dengan teknologi deteksi terbukti
        </p>
      </div>

      <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">

        <div 
          v-for="(feature, index) in features" 
          :key="index"
          ref="cardRefs" 
          class="feature-card bg-[#1A1A2E] rounded-2xl p-8 border border-[#33333C] hover:border-[#4D41C0] hover:shadow-[0_0_30px_rgba(77,65,192,0.5)] transition-all duration-300 group"
          :style="{ animationDelay: `${index * 0.2}s` }"
        >
          <div class="w-16 h-16 bg-[#4D41C0] rounded-xl flex items-center justify-center mb-6 group-hover:shadow-[0_0_20px_rgba(77,65,192,0.6)] transition-all duration-300">
            <svg class="w-8 h-8 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24" v-html="feature.icon">
            </svg>
          </div>
          <h3 class="text-xl font-bold text-white mb-3">
            {{ feature.title }}
          </h3>
          <p class="text-gray-400 leading-relaxed">
            {{ feature.description }}
          </p>
        </div>

      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'

const cardRefs = ref([])

const features = [
  {
    title: "Deteksi Langsung",
    description: "Identifikasi instan api dan asap menggunakan algoritma AI canggih dengan waktu respons milidetik.",
    icon: '<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"/>'
  },
  {
    title: "Integrasi Multi-Kamera",
    description: "Hubungkan dan pantau umpan beberapa kamera secara bersamaan di seluruh fasilitas Anda dengan mulus.",
    icon: '<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 10l4.553-2.276A1 1 0 0121 8.618v6.764a1 1 0 01-1.447.894L15 14M5 18h8a2 2 0 002-2V8a2 2 0 00-2-2H5a2 2 0 00-2 2v8a2 2 0 002 2z"/>'
  },
  {
    title: "Dasbor Analitik",
    description: "Visualisasi data komprehensif dan alat pelaporan untuk melacak insiden dan kinerja sistem.",
    icon: '<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z"/>'
  },
  {
    title: "Ambang Peringatan Kustom",
    description: "Konfigurasikan sensitivitas deteksi dan parameter peringatan yang disesuaikan dengan lingkungan spesifik Anda.",
    icon: '<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10.325 4.317c.426-1.756 2.924-1.756 3.35 0a1.724 1.724 0 002.573 1.066c1.543-.94 3.31.826 2.37 2.37a1.724 1.724 0 001.065 2.572c1.756.426 1.756 2.924 0 3.35a1.724 1.724 0 00-1.066 2.573c.94 1.543-.826 3.31-2.37 2.37a1.724 1.724 0 00-2.572 1.065c-.426 1.756-2.924 1.756-3.35 0a1.724 1.724 0 00-2.573-1.066c-1.543.94-3.31-.826-2.37-2.37a1.724 1.724 0 00-1.065-2.572c-1.756-.426-1.756-2.924 0-3.35a1.724 1.724 0 001.066-2.573c-.94-1.543.826-3.31 2.37-2.37.996.608 2.296.07 2.572-1.065z"/><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z"/>'
  }
]

onMounted(() => {
  const observer = new IntersectionObserver(
    (entries) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) {
          entry.target.classList.add('animate')
          observer.unobserve(entry.target)
        }
      })
    },
    { threshold: 0.1 }
  )

  if (Array.isArray(cardRefs.value)) {
    cardRefs.value.forEach((card) => {
      if (card) observer.observe(card)
    })
  }
})
</script>

<style scoped>
.feature-card {
  opacity: 0;
  transform: translateY(20px);
}

/* Class added by IntersectionObserver */
.feature-card.animate {
    animation: fadeInUp 0.6s ease-out forwards;
}

@keyframes fadeInUp {
  to {
    opacity: 1;
    transform: translateY(0);
  }
}
</style>
