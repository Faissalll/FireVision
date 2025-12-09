<template>
  <div ref="sectionRef" class="relative py-24 px-6 overflow-hidden">
    
    <!-- Background Elements matched to TSX: rounded-full blur-[150px] opacity-10 -->
    <div class="absolute top-40 right-0 w-96 h-96 bg-[#5d51e8] rounded-full blur-[150px] opacity-10 pointer-events-none"></div>

    <div class="container mx-auto max-w-7xl relative z-10">
      
      <!-- Section Header -->
      <div v-if="showTitle" class="text-center mb-16">
        <h2 class="mb-4 bg-gradient-to-r from-white to-[#cfcfcf] bg-clip-text text-transparent font-bold" style="font-size: 3rem; font-weight: 700;">
          Fitur Ampuh untuk Perlindungan Lengkap
        </h2>
        <p class="text-[#cfcfcf] max-w-2xl mx-auto" style="font-size: 1.25rem;">
          FireVision menggabungkan teknologi AI mutakhir dengan keandalan tingkat perusahaan untuk menghadirkan sistem deteksi kebakaran tercanggih yang tersedia.
        </p>
      </div>

      <!-- Features Grid -->
      <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        
        <div 
          v-for="(feature, index) in features" 
          :key="index"
          class="relative group backdrop-blur-xl bg-white/5 border border-white/10 hover:border-[#5d51e8]/50 transition-all duration-300 hover:shadow-2xl hover:shadow-[#5d51e8]/20 cursor-pointer overflow-hidden rounded-xl feature-card"
        >
          <!-- Hover Glow Effect -->
          <div class="absolute inset-0 bg-gradient-to-br from-[#5d51e8]/10 to-transparent opacity-0 group-hover:opacity-100 transition-opacity duration-300 pointer-events-none"></div>
          
          <div class="relative p-8">
            <!-- Icon with Glow -->
            <div class="mb-6">
              <div class="relative inline-block">
                <div class="absolute inset-0 bg-[#5d51e8] rounded-lg blur-xl opacity-0 group-hover:opacity-50 transition-opacity duration-300"></div>
                <div class="relative bg-gradient-to-br from-[#5d51e8] to-[#4a3eb8] p-4 rounded-lg">
                  <!-- Render SVG Icon -->
                  <svg class="w-8 h-8 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24" v-html="feature.icon"></svg>
                </div>
              </div>
            </div>

            <!-- Content -->
            <h3 class="mb-3 text-white" style="font-size: 1.25rem; font-weight: 600;">
              {{ feature.title }}
            </h3>
            <p class="text-[#cfcfcf]">
              {{ feature.description }}
            </p>
          </div>
        </div>

      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'

const sectionRef = ref(null)

const props = defineProps({
  showTitle: {
    type: Boolean,
    default: true
  }
})

// Features data mapped to the structure of the TSX but with Indonesian content
const features = [
  {
    title: "Deteksi Real-Time",
    description: "Identifikasi instan api dan asap menggunakan algoritma AI canggih dengan waktu respons milidetik.",
    // Lucide Search Icon equivalent
    icon: '<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"/>' 
  },
  {
    title: "Integrasi Multi-Kamera",
    description: "Hubungkan dan pantau beberapa feed kamera secara bersamaan di seluruh fasilitas Anda dengan mulus.",
    // Lucide Video Icon equivalent
    icon: '<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 10l4.553-2.276A1 1 0 0121 8.618v6.764a1 1 0 01-1.447.894L15 14M5 18h8a2 2 0 002-2V8a2 2 0 00-2-2H5a2 2 0 00-2 2v8a2 2 0 002 2z"/>' 
  },
  {
    title: "Dashboard Analitik",
    description: "Visualisasi data komprehensif dan alat pelaporan untuk melacak insiden dan kinerja sistem.",
    // Lucide BarChart3 Icon equivalent
    icon: '<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 3v18h18"/><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M18 17V9"/><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 17V5"/><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 17v-3"/>'
  },
  {
    title: "Kustomisasi Peringatan",
    description: "Konfigurasikan sensitivitas deteksi dan parameter peringatan yang disesuaikan dengan lingkungan spesifik Anda.",
    // Lucide Settings Icon equivalent
    icon: '<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12.22 2h-.44a2 2 0 00-2 2v.18a2 2 0 01-1 1.73l-.43.25a2 2 0 01-2 0l-.18-.08a2 2 0 00-2 2v.45a2 2 0 002 2h.2a2 2 0 012 2v1a2 2 0 002 2h1a2 2 0 002-2v-1a2 2 0 012-2h.2a2 2 0 002-2v-.45a2 2 0 00-2-2l-.18.08a2 2 0 01-2 0l-.43-.25a2 2 0 01-1-1.73V4a2 2 0 00-2-2z"/><circle cx="12" cy="12" r="3" stroke-linecap="round" stroke-linejoin="round" stroke-width="2"/>' 
  }
]

onMounted(() => {
  if (!sectionRef.value) return;

  const cards = sectionRef.value.querySelectorAll('.feature-card');
  const observer = new IntersectionObserver(
    (entries) => {
      entries.forEach((entry, index) => {
        if (entry.isIntersecting) {
          entry.target.style.transitionDelay = `${index * 0.1}s`
          entry.target.classList.remove('prepare-animate') 
          entry.target.classList.add('animate')
          observer.unobserve(entry.target)
        }
      })
    },
    { threshold: 0.1 }
  )

  cards.forEach((card) => {
    card.classList.add('prepare-animate');
    observer.observe(card);
  })
})
</script>

<style scoped>
.feature-card {
  opacity: 1;
  transform: translateY(0);
  transition: all 0.5s ease-out;
}

.feature-card.prepare-animate {
    opacity: 0;
    transform: translateY(30px);
}

.feature-card.animate {
  opacity: 1;
  transform: translateY(0);
}
</style>
