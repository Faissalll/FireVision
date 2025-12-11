<template>
    <div class="min-h-screen bg-[#050716] text-white font-sans selection:bg-[#6C4DFF] selection:text-white flex flex-col">
        <Navbar />
        <AboutContent />
        <Footer />
    </div>
</template>

<script setup>
import Navbar from '../components/Navbar.vue';
import Footer from '../components/Footer.vue';
import AboutContent from '../components/Footer Component/AboutContent.vue';
</script>
