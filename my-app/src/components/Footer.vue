<template>
  <footer class="bg-[#0F0F1A] text-gray-400">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-16">
      
      <div class="grid grid-cols-1 md:grid-cols-6 gap-8">
        
        <div class="md:col-span-2">
          <div class="flex items-center space-x-3 mb-5">
            <div class="w-10 h-10 bg-[#4D41C0] rounded-lg flex items-center justify-center p-2">
              <img 
                src="../assets/LogoWeb.png" 
                alt="FireVision Logo" 
                class="w-full h-full object-contain"
              />
            </div>
            <span class="font-bold text-2xl text-white">FireVision</span>
          </div>
          
          <p class="text-sm text-gray-400 mb-6 max-w-xs">
            Deteksi api dan asap bertenaga AI untuk dunia modern. Melindungi nyawa dan properti dengan teknologi mutakhir.
          </p>
          
          <div class="flex space-x-3">
            <a v-for="icon in socialIcons" :key="icon.name" :href="icon.href"
               class="bg-[#1F1F2B] p-2 rounded-full hover:bg-gray-700 transition-colors duration-200">
              <span class="sr-only">{{ icon.name }}</span>
              <svg class="w-5 h-5 text-gray-300" fill="currentColor" viewBox="0 0 24 24" aria-hidden="true" v-html="icon.svgPath"></svg>
            </a>
          </div>
        </div>
        
        <div>
          <h3 class="text-sm font-semibold text-white tracking-wider uppercase mb-4">Halaman</h3>
          <ul class="space-y-3">
            <li v-for="item in productLinks" :key="item.name">
              <button 
                @click="navigateTo(item.path)" 
                class="text-sm text-gray-400 hover:text-white transition-colors duration-200 text-left"
              >
                {{ item.name }}
              </button>
            </li>
          </ul>
        </div>
        
        <div>
          <h3 class="text-sm font-semibold text-white tracking-wider uppercase mb-4">Perusahaan</h3>
          <ul class="space-y-3">
            <li v-for="item in companyLinks" :key="item.name">
              <a :href="item.href" class="text-sm hover:text-white transition-colors duration-200">{{ item.name }}</a>
            </li>
          </ul>
        </div>
        
        <div>
          <h3 class="text-sm font-semibold text-white tracking-wider uppercase mb-4">Sumber Daya</h3>
          <ul class="space-y-3">
            <li v-for="item in resourceLinks" :key="item.name">
              <a :href="item.href" class="text-sm hover:text-white transition-colors duration-200">{{ item.name }}</a>
            </li>
          </ul>
        </div>
        
        <div>
          <h3 class="text-sm font-semibold text-white tracking-wider uppercase mb-4">Legal</h3>
          <ul class="space-y-3">
            <li v-for="item in legalLinks" :key="item.name">
              <a :href="item.href" class="text-sm hover:text-white transition-colors duration-200">{{ item.name }}</a>
            </li>
          </ul>
        </div>
        
      </div>
      
      <hr class="mt-12 border-gray-800" />
      
      <div class="mt-8 flex flex-col md:flex-row md:items-center md:justify-between">
        <p class="text-sm text-gray-500 text-center md:text-left">
          &copy; 2025 FireVision. Hak cipta dilindungi undang-undang.
        </p>
        <p class="text-sm text-gray-500 mt-4 md:mt-0 text-center md:text-right">
        </p>
      </div>
      
    </div>
  </footer>
</template>

<script setup>
import { useRouter, useRoute } from 'vue-router';

const router = useRouter();
const route = useRoute();

const navigateTo = (path) => {
    router.push(path);
};

const isActive = (path) => {
    return route.path === path;
};

const productLinks = [
  { name: 'Beranda', path: '/' },
  { name: 'Fitur', path: '/features' },
  { name: 'Harga', path: '/pricing' },
  { name: 'Demo', path: '/demo' },
  { name: 'Cara Kerja', path: '/how-it-works' },
]

const companyLinks = [
  { name: 'Tentang', href: '#' },
  { name: 'Blog', href: '#' },
  { name: 'Karir', href: '#' },
  { name: 'Kontak', href: '#' },
]

const resourceLinks = [
  { name: 'Dokumentasi', href: '#' },
  { name: 'Referensi API', href: '#' },
  { name: 'Dukungan', href: '#' },
  { name: 'Komunitas', href: '#' },
]

const legalLinks = [
  { name: 'Privasi', href: '#' },
  { name: 'Syarat', href: '#' },
  { name: 'Keamanan', href: '#' },
  { name: 'Kepatuhan', href: '#' },
]

const socialIcons = [
  { 
    name: 'Twitter', 
    href: '#', 
    svgPath: '<path d="M8.29 20.251c7.547 0 11.675-6.253 11.675-11.675 0-.178 0-.355-.012-.53A8.348 8.348 0 0022 5.92a8.19 8.19 0 01-2.357.646 4.118 4.118 0 001.804-2.27 8.224 8.224 0 01-2.605.996 4.107 4.107 0 00-6.993 3.743 11.65 11.65 0 01-8.457-4.287 4.106 4.106 0 001.27 5.477A4.072 4.072 0 012.8 9.713v.052a4.105 4.105 0 003.292 4.022 4.095 4.095 0 01-1.853.07 4.108 4.108 0 003.834 2.85A8.233 8.233 0 012 18.407a11.616 11.616 0 006.29 1.84"></path>' 
  },
  { 
    name: 'LinkedIn', 
    href: '#', 
    svgPath: '<path fill-rule="evenodd" d="M19 0h-14c-2.761 0-5 2.239-5 5v14c0 2.761 2.239 5 5 5h14c2.762 0 5-2.239 5-5v-14c0-2.761-2.238-5-5-5zm-11 19h-3v-11h3v11zm-1.5-12.268c-.966 0-1.75-.79-1.75-1.764s.784-1.764 1.75-1.764 1.75.79 1.75 1.764-.783 1.764-1.75 1.764zm13.5 12.268h-3v-5.604c0-3.368-4-3.113-4 0v5.604h-3v-11h3v1.765c1.396-2.586 7-2.777 7 2.476v6.759z" clip-rule="evenodd"></path>' 
  },
  { 
    name: 'GitHub', 
    href: '#', 
    svgPath: '<path fill-rule="evenodd" d="M12 2C6.477 2 2 6.477 2 12c0 4.418 2.865 8.165 6.839 9.489.5.092.682-.217.682-.482 0-.237-.009-.868-.013-1.703-2.782.605-3.369-1.343-3.369-1.343-.454-1.158-1.11-1.466-1.11-1.466-.908-.62.069-.608.069-.608 1.003.07 1.531 1.032 1.531 1.032.892 1.53 2.341 1.088 2.91.832.092-.647.35-1.088.636-1.338-2.22-.253-4.555-1.11-4.555-4.951 0-1.093.39-1.988 1.03-2.688-.103-.253-.446-1.272.098-2.65 0 0 .84-.27 2.75 1.026A9.564 9.564 0 0112 6.844c.85.004 1.705.115 2.504.337 1.909-1.296 2.747-1.026 2.747-1.026.546 1.379.202 2.398.1 2.65.64.7 1.028 1.595 1.028 2.688 0 3.848-2.339 4.695-4.566 4.942.359.309.678.92.678 1.855 0 1.338-.012 2.419-.012 2.747 0 .268.18.58.688.482A10.001 10.001 0 0022 12c0-5.523-4.477-10-10-10z" clip-rule="evenodd"></path>' 
  },
  { 
    name: 'Email', 
    href: '#', 
    svgPath: '<path d="M2.003 5.884L10 13.783l7.997-7.9V20H2V5.884zM19.997 4H4v.884l8 7.997 8-7.997V4z"></path>' 
  }
]
</script>

<style scoped>
</style>