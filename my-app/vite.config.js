import { defineConfig } from "vite";
import vue from "@vitejs/plugin-vue";
import tailwindcss from "@tailwindcss/vite";

export default defineConfig({
    // *** PERUBAHAN PENTING DI SINI ***
    // Properti base: './' atau base: '/' menentukan awalan path aset.
    // Jika menggunakan Mode Hash di lokal, kita akan pastikan base tetap '/'
    // untuk aset dimuat dari root, atau menggunakan path relatif yang benar.

    // Karena kita ingin agar aset selalu dimuat dari akar (root) server dev,
    // dan ini mencegah masalah aset hilang saat Mode Hash digunakan.
    // Base must be '/' for Vercel root deployment
    base: "/",

    plugins: [vue(), tailwindcss()],
});
