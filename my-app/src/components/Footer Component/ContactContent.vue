<template>
    <div class="flex-grow pt-24 pb-12 px-4 sm:px-6 lg:px-8 max-w-4xl mx-auto w-full">
        <button @click="$router.back()" class="flex items-center gap-2 text-gray-400 hover:text-white mb-8 transition-colors group">
            <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="group-hover:-translate-x-1 transition-transform"><path d="m15 18-6-6 6-6"/></svg>
            Kembali
        </button>
        <h1 class="text-4xl font-bold mb-6 bg-gradient-to-r from-white to-gray-400 bg-clip-text text-transparent">Hubungi Kami</h1>
        
        <div class="grid grid-cols-1 md:grid-cols-2 gap-12 mt-8">
            <div>
                <h2 class="text-2xl font-semibold text-white mb-4">Kantor Pusat</h2>
                <p class="text-gray-400 mb-2">Gedung Teknologi Masa Depan, Lt. 12</p>
                <p class="text-gray-400 mb-2">Jl. Jenderal Sudirman No. 1</p>
                <p class="text-gray-400 mb-6">Balikpapan City, East Kalimantan, 76114</p>
                
                <h2 class="text-2xl font-semibold text-white mb-4">Kontak Langsung</h2>
                <p class="text-gray-400 mb-2">Email: <a href="mailto:support@firevision.id" class="text-[#6C4DFF] hover:underline">support@firevision.id</a></p>
                <p class="text-gray-400">Telepon: +62 542 123456</p>
            </div>
            
            <div class="bg-[#1A1A2E] p-6 rounded-xl border border-gray-800">
                <form @submit.prevent="submitForm" class="space-y-4">
                    <div>
                        <label class="block text-sm font-medium text-gray-400 mb-1">Nama</label>
                        <input type="text" class="w-full bg-[#0F0F1A] border border-gray-700 rounded-lg px-4 py-2 text-white focus:border-[#6C4DFF] focus:outline-none" placeholder="Nama Anda">
                    </div>
                    <div>
                        <label class="block text-sm font-medium text-gray-400 mb-1">Email</label>
                        <input type="email" class="w-full bg-[#0F0F1A] border border-gray-700 rounded-lg px-4 py-2 text-white focus:border-[#6C4DFF] focus:outline-none" placeholder="email@contoh.com">
                    </div>
                    <div>
                        <label class="block text-sm font-medium text-gray-400 mb-1">Pesan</label>
                        <textarea rows="4" class="w-full bg-[#0F0F1A] border border-gray-700 rounded-lg px-4 py-2 text-white focus:border-[#6C4DFF] focus:outline-none" placeholder="Tulis pesan Anda..."></textarea>
                    </div>
                    <button class="w-full bg-[#6C4DFF] hover:bg-[#5a3fe0] text-white font-bold py-2 rounded-lg transition-colors">
                        Kirim Pesan
                    </button>
                </form>
            </div>
        </div>
    </div>
</template>

<script setup>
const submitForm = () => {
    alert("Terima kasih! Pesan Anda telah kami terima (Simulasi).");
};
</script>
