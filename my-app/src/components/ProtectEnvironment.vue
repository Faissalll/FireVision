<template>
  <div ref="sectionRef" class="bg-[#0F0F1E] py-20 px-4">
    <div class="max-w-4xl mx-auto">
      
      <div class="cta-card bg-gradient-to-br from-[#2A2A3E] to-[#1A1A2E] rounded-3xl p-12 md:p-16 border border-[#33333C] shadow-2xl">
        
        <div class="flex justify-center mb-8">
          <div class="w-20 h-20 bg-[#4D41C0] rounded-full flex items-center justify-center shadow-lg">
            <svg class="w-10 h-10 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z"/>
            </svg>
          </div>
        </div>

        <h2 class="text-4xl md:text-5xl font-bold text-white text-center mb-6">
          Lindungi Lingkungan Anda dengan<br>FireVision AI
        </h2>

        <p class="text-xl text-gray-300 text-center mb-10 max-w-2xl mx-auto">
          Bergabunglah dengan ribuan organisasi di seluruh dunia yang menggunakan deteksi kebakaran bertenaga AI.<br>
          Mulai hari ini dengan konsultasi dan demo gratis.
        </p>

        <div class="flex flex-col sm:flex-row items-center justify-center gap-4 mb-12">
          <button @click="$router.push('/demo')" class="bg-[#4D41C0] text-white px-8 py-4 rounded-lg font-semibold text-lg transition-all duration-300 shadow-lg hover:shadow-2xl hover:shadow-[#4D41C0]/60 hover:scale-[1.02] flex items-center gap-2 group">
            <span>Mulai Sekarang</span>
            <svg class="w-5 h-5 group-hover:translate-x-1 transition-transform duration-300" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 7l5 5m0 0l-5 5m5-5H6"/>
            </svg>
          </button>
          
          <button @click="$router.push('/features')" class="bg-transparent border-2 border-gray-500 text-white px-8 py-4 rounded-lg font-semibold text-lg transition-all duration-300 hover:border-[#4D41C0] hover:bg-[#4D41C0]/10 hover:scale-[1.02]">
            Pelajari Lebih Lanjut
          </button>
        </div>

        <div class="w-full h-px bg-gradient-to-r from-transparent via-[#33333C] to-transparent mb-8"></div>

        <div class="flex flex-col md:flex-row items-center justify-center gap-8 text-center">
          
          <div class="flex items-center gap-2">
            <div class="w-2 h-2 bg-[#4D41C0] rounded-full"></div>
            <span class="text-gray-300 font-medium">Dukungan 24/7</span>
          </div>

          <div class="flex items-center gap-2">
            <div class="w-2 h-2 bg-[#4D41C0] rounded-full"></div>
            <span class="text-gray-300 font-medium">Uptime 99.9%</span>
          </div>

          <div class="flex items-center gap-2">
            <div class="w-2 h-2 bg-[#4D41C0] rounded-full"></div>
            <span class="text-gray-300 font-medium">Keamanan Tingkat Perusahaan</span>
          </div>

        </div>

      </div>

    </div>
  </div>
</template>

<script setup>
import { onMounted, ref } from 'vue';
import { useRouter } from 'vue-router';

const router = useRouter(); // Although $router works in template, good practice to have it available
const sectionRef = ref(null);

onMounted(() => {
    if (!sectionRef.value) return;

    // Use scoped querySelector for reliability
    const card = sectionRef.value.querySelector('.cta-card');
    
    if (card) {
        const observer = new IntersectionObserver((entries) => {
            entries.forEach((entry) => {
                if (entry.isIntersecting) {
                    entry.target.classList.remove('prepare-animate');
                    entry.target.classList.add('animate');
                    observer.unobserve(entry.target);
                }
            });
        }, {
            threshold: 0.1
        });

        card.classList.add('prepare-animate');
        observer.observe(card);

        // Failsafe: Force show after 3 seconds
        setTimeout(() => {
             card.classList.remove('prepare-animate');
             card.classList.add('animate');
        }, 3000);
    }
});
</script>

<style scoped>
.cta-card {
    opacity: 1;
    transform: scale(1);
    transition: all 0.8s cubic-bezier(0.22, 1, 0.36, 1);
}

.cta-card.prepare-animate {
    opacity: 0;
    transform: scale(0.95) translateY(30px);
}

.cta-card.animate {
    opacity: 1;
    transform: scale(1) translateY(0);
}
</style>