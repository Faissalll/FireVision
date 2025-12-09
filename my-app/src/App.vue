<script setup>
import Navbar from "./components/Navbar.vue";
</script>

<template>
    <div class="min-h-screen bg-[#0F0F1E] text-gray-100">
        <Navbar />
        <main class="pt-16">
            <router-view />
        </main>
    </div>
</template>
