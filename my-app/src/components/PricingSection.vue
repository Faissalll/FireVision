<script setup>
const plans = [
  {
    name: "Starter",
    description: "Sempurna untuk bisnis kecil dan operasi satu lokasi",
    price: "Rp 299rb",
    period: "/bulan",
    isPopular: false,
    buttonText: "Mulai Uji Coba Gratis",
    buttonVariant: "outline",
    icon: "zap",
    features: [
      { text: "Hingga 4 kamera", included: true },
      { text: "Deteksi real-time", included: true },
      { text: "Notifikasi Email & SMS", included: true },
      { text: "Dashboard analitik dasar", included: true },
      { text: "Akses aplikasi mobile", included: true },
      { text: "SLA uptime 99.5%", included: true },
      { text: "Dukungan Email", included: true },
      { text: "Penyimpanan cloud (30 hari)", included: true },
      { text: "Pelatihan AI kustom", included: false },
      { text: "Analitik lanjutan", included: false },
      { text: "Akses API", included: false },
      { text: "Dukungan khusus", included: false },
    ]
  },
  {
    name: "Professional",
    description: "Ideal untuk bisnis berkembang dengan banyak lokasi",
    price: "Rp 799rb",
    period: "/bulan",
    isPopular: true,
    buttonText: "Mulai Uji Coba Gratis",
    buttonVariant: "solid",
    icon: "layers",
    features: [
      { text: "Hingga 20 kamera", included: true },
      { text: "Deteksi real-time", included: true },
      { text: "Notifikasi multi-saluran", included: true },
      { text: "Analitik lanjutan", included: true },
      { text: "Aplikasi mobile & web", included: true },
      { text: "SLA uptime 99.9%", included: true },
      { text: "Dukungan prioritas", included: true },
      { text: "Penyimpanan cloud (90 hari)", included: true },
      { text: "Aturan notifikasi kustom", included: true },
      { text: "Dukungan integrasi", included: true },
      { text: "Kolaborasi tim", included: true },
      { text: "Laporan bulanan", included: true },
      { text: "Pelatihan AI kustom", included: false },
      { text: "Opsi white-label", included: false },
    ]
  },
  {
    name: "Enterprise",
    description: "Solusi komprehensif untuk organisasi besar",
    price: "Custom",
    period: "",
    isPopular: false,
    buttonText: "Hubungi Sales",
    buttonVariant: "outline",
    icon: "rocket",
    features: [
      { text: "Kamera tak terbatas", included: true },
      { text: "Deteksi real-time", included: true },
      { text: "Semua saluran notifikasi", included: true },
      { text: "Suite analitik lengkap", included: true },
      { text: "Aplikasi mobile kustom", included: true },
      { text: "SLA uptime 99.99%", included: true },
      { text: "Dukungan khusus 24/7", included: true },
      { text: "Penyimpanan cloud tak terbatas", included: true },
      { text: "Pelatihan AI kustom", included: true },
      { text: "Akses API penuh", included: true },
      { text: "Opsi white-label", included: true },
      { text: "Deployment on-premise", included: true },
      { text: "Integrasi kustom", included: true },
      { text: "Laporan kepatuhan", included: true },
      { text: "Manajer akun khusus", included: true },
    ]
  }
];
</script>

<template>
  <section class="py-20 relative overflow-hidden">
    <!-- Header -->
    <div class="text-center mb-24 relative z-10 px-4">
      <h2 class="text-3xl md:text-5xl font-bold mb-4 text-white">
        Harga Simpel & Transparan
      </h2>
      <p class="text-gray-400 text-lg md:text-xl max-w-2xl mx-auto">
        Pilih paket yang sempurna untuk kebutuhan keamanan api Anda. Semua paket termasuk uji coba gratis 14 hari.
      </p>
    </div>

    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      <div class="grid grid-cols-1 lg:grid-cols-3 gap-8">
        
        <div v-for="(plan, index) in plans" :key="index" 
             class="relative flex flex-col p-8 rounded-2xl transition-transform duration-300 hover:-translate-y-2 border"
             :class="[
               plan.isPopular 
                 ? 'bg-[#0B0F1A]/80 border-[#6C4DFF] shadow-[0_0_30px_rgba(108,77,255,0.15)] z-10 scale-105 lg:scale-105' 
                 : 'bg-[#0B0F1A] border-gray-800 hover:border-gray-700'
             ]">
          
          <!-- Most Popular Badge -->
          <div v-if="plan.isPopular" class="absolute -top-4 left-0 right-0 flex justify-center">
            <span class="bg-[#6C4DFF] text-white text-xs font-bold px-4 py-1 rounded-full uppercase tracking-wider shadow-lg">
              Paling Populer
            </span>
          </div>

          <!-- Icon -->
          <div class="w-12 h-12 rounded-xl flex items-center justify-center mb-6"
               :class="plan.isPopular ? 'bg-[#6C4DFF] text-white' : 'bg-[#6C4DFF]/20 text-[#6C4DFF]'">
             <svg v-if="plan.icon === 'zap'" xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polygon points="13 2 3 14 12 14 11 22 21 10 12 10 13 2"/></svg>
             <svg v-if="plan.icon === 'layers'" xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polygon points="12 2 2 7 12 12 22 7 12 2"/><polyline points="2 17 12 22 22 17"/><polyline points="2 12 12 17 22 12"/></svg>
             <svg v-if="plan.icon === 'rocket'" xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M4.5 16.5c-1.5 1.26-2 5-2 5s3.74-.5 5-2c.71-.84.7-2.13-.09-2.91a2.18 2.18 0 0 0-2.91-.09z"/><path d="m12 15-3-3a22 22 0 0 1 2-3.95A12.88 12.88 0 0 1 22 2c0 2.72-.78 7.5-6 11a22.35 22.35 0 0 1-4 2z"/><path d="M9 12H4s.55-3.03 2-4c1.62-1.1 4-1 4-1"/><path d="M12 15v5s3.03-.55 4-2c1.1-1.62 1-4 1-4"/></svg>
          </div>

          <!-- Title & Desc -->
          <h3 class="text-xl font-bold text-white mb-2">{{ plan.name }}</h3>
          <p class="text-gray-400 text-sm mb-6 h-10">{{ plan.description }}</p>

          <!-- Price -->
          <div class="flex items-baseline mb-6">
            <span class="text-4xl font-bold text-white">{{ plan.price }}</span>
            <span class="text-gray-500 ml-2">{{ plan.period }}</span>
          </div>

          <!-- Button -->
          <button class="w-full py-3 rounded-lg font-semibold transition-all duration-300 mb-8"
                  :class="[
                    plan.buttonVariant === 'solid' 
                      ? 'bg-[#6C4DFF] hover:bg-[#5839EE] text-white shadow-lg shadow-[#6C4DFF]/30' 
                      : 'bg-transparent border border-gray-600 hover:border-gray-400 text-white hover:bg-gray-800'
                  ]">
            {{ plan.buttonText }}
          </button>

          <!-- Features -->
          <ul class="space-y-4 flex-1">
            <li v-for="(feature, fIndex) in plan.features" :key="fIndex" class="flex items-start gap-3">
              <div class="mt-0.5 shrink-0">
                <svg v-if="feature.included" xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#6C4DFF" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"><polyline points="20 6 9 17 4 12"/></svg>
                <svg v-else xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#4B5563" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"><line x1="18" y1="6" x2="6" y2="18"></line><line x1="6" y1="6" x2="18" y2="18"></line></svg>
              </div>
              <span class="text-sm" :class="feature.included ? 'text-gray-300' : 'text-gray-600 line-through decoration-gray-600'">
                {{ feature.text }}
              </span>
            </li>
          </ul>

        </div>

      </div>
    </div>
  </section>
</template>
