<script setup>
import Navbar from '../components/Navbar.vue';
import Footer from '../components/Footer.vue';
import PricingSection from '../components/PricingSection.vue';
</script>

<template>
    <div class="min-h-screen bg-[#050716] text-white font-sans selection:bg-[#6C4DFF] selection:text-white overflow-x-hidden">
        <Navbar />
        
        <!-- Main Content -->
        <main>
            <PricingSection />
        </main>
        
        <Footer />
    </div>
</template>
