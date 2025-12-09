<script setup>
import Navbar from '../components/Navbar.vue';
import Footer from '../components/Footer.vue';
import NotificationPreferences from '../components/NotificationPreferences.vue';
</script>

<template>
    <div class="min-h-screen bg-[#050716] text-white font-sans selection:bg-[#6C4DFF] selection:text-white overflow-x-hidden">
        <Navbar />

        <div class="pt-12 pb-12 px-4 sm:px-6 lg:px-8 max-w-7xl mx-auto">
            
            <!-- Header -->
            <div class="mb-10 animate-fade-in-down">
                <button @click="$router.back()" class="flex items-center gap-2 text-gray-400 hover:text-white mb-4 transition-colors group">
                    <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="group-hover:-translate-x-1 transition-transform"><path d="m15 18-6-6 6-6"/></svg>
                    Kembali
                </button>
                <h1 class="text-3xl md:text-4xl font-bold mb-3 bg-gradient-to-r from-white to-gray-400 bg-clip-text text-transparent">
                    Pengaturan Notifikasi & Alarm
                </h1>
                <p class="text-gray-400 text-lg">
                    Atur cara FireVision mengirim peringatan kebakaran kepada Anda.
                </p>
            </div>

            <!-- Content Component -->
            <NotificationPreferences />

        </div>
        
        <Footer />
    </div>
</template>

<style scoped>
@keyframes fadeInDown {
    from {
        opacity: 0;
        transform: translateY(-20px);
    }
    to {
        opacity: 1;
        transform: translateY(0);
    }
}

.animate-fade-in-down {
    animation: fadeInDown 0.6s ease-out forwards;
}
</style>
