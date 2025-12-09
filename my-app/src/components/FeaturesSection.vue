<template>
  <div ref="sectionRef" class="bg-[#0F0F1E] py-20 px-4">
    <div class="max-w-7xl mx-auto">

      <!-- Top Title (Conditional) -->
      <div v-if="titlePosition === 'top'" class="text-center mb-8">
        <h2 class="text-4xl md:text-5xl font-bold text-white mb-4">
          Fitur Canggih
        </h2>
        <p class="text-xl text-gray-400">
          FireVision menggabungkan AI mutakhir dengan teknologi deteksi terbukti
        </p>
      </div>

      <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">

        <div 
          v-for="(feature, index) in features" 
          :key="index"
          class="feature-card bg-[#1A1A2E] rounded-2xl p-8 border border-[#33333C] hover:border-[#4D41C0] hover:shadow-[0_0_30px_rgba(77,65,192,0.5)] transition-all duration-300 group"
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

      <!-- Bottom Title (Conditional) -->
      <div v-if="titlePosition === 'bottom'" class="text-center">
        <h2 class="text-4xl md:text-5xl font-bold text-white mb-4">
          Fitur Canggih
        </h2>
        <p class="text-xl text-gray-400">
          FireVision menggabungkan AI mutakhir dengan teknologi deteksi terbukti
        </p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'

const sectionRef = ref(null)

const props = defineProps({
  titlePosition: {
    type: String,
    default: 'bottom'
  }
})

const features = [
  {
    title: "Deteksi Cepat Kilat",
    description: "Memproses umpan video secara real-time dengan waktu respons di bawah 1 detik untuk pencegahan dini.",
    icon: '<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z"/>'
  },
  {
    title: "Tingkat Akurasi 99.9%",
    description: "Model deep learning canggih yang dilatih pada jutaan dataset untuk meminimalkan alarm palsu.",
    icon: '<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"/>'
  },
  {
    title: "Dasbor Analitik",
    description: "Pantau status keamanan fasilitas Anda dalam satu tampilan terpusat dengan statistik real-time.",
    icon: '<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z"/>'
  },
  {
    title: "Integrasi Multi-Kamera",
    description: "Satu sistem untuk semua kamera. Gabungkan CCTV gudang, kantor, dan area luar dalam satu layar pemantauan yang mudah.",
    icon: '<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 10l4.553-2.276A1 1 0 0121 8.618v6.764a1 1 0 01-1.447.894L15 14M5 18h8a2 2 0 002-2V8a2 2 0 00-2-2H5a2 2 0 00-2 2v8a2 2 0 002 2z"/>'
  }
]

onMounted(() => {
  if (!sectionRef.value) return;

  const cards = sectionRef.value.querySelectorAll('.feature-card');

  const observer = new IntersectionObserver(
    (entries) => {
      entries.forEach((entry, index) => {
        if (entry.isIntersecting) {
          entry.target.style.transitionDelay = `${index * 0.2}s`
          entry.target.classList.remove('prepare-animate')
          entry.target.classList.add('animate')
          observer.unobserve(entry.target)
        }
      })
    },
    { threshold: 0.1 }
  )

  cards.forEach((card) => {
    card.classList.add('prepare-animate')
    observer.observe(card)
  })
})
</script>

<style scoped>
.feature-card {
  opacity: 1;
  transform: translateY(0);
  transition: opacity 0.6s ease-out, transform 0.6s ease-out;
}

.feature-card.prepare-animate {
    opacity: 0;
    transform: translateY(20px);
}

.feature-card.animate {
  opacity: 1;
  transform: translateY(0);
}
</style>
