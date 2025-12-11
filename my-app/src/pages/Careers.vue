<template>
    <div class="min-h-screen bg-[#050716] text-white font-sans selection:bg-[#6C4DFF] selection:text-white flex flex-col">
        <Navbar />
        <CareersContent />
        <Footer />
    </div>
</template>

<script setup>
import Navbar from '../components/Navbar.vue';
import Footer from '../components/Footer.vue';
import CareersContent from '../components/Footer Component/CareersContent.vue';
</script>
