<script setup>
import Navbar from "./components/Navbar.vue";
</script>

<template>
    <div class="min-h-screen bg-[#0F0F1E] text-gray-100">
        <Navbar />
        <!-- HAPUS pt-20 / pt-16 kalau ada -->
        <main>
            <router-view />
        </main>
    </div>
</template>
