<script setup>
import { ref, onMounted } from "vue";
import { useRouter, useRoute } from "vue-router";

const isMenuOpen = ref(false);
const router = useRouter();
const route = useRoute();
const user = ref(null);

onMounted(() => {
    // Check localstorage
    const stored = localStorage.getItem("user");
    if (stored) {
        user.value = JSON.parse(stored);
    }
});

const getDisplayName = (username) => {
    if (!username) return "";
    return username.split('@')[0];
};

const handleLogout = () => {
    localStorage.removeItem("user");
    user.value = null; // Update local state immediately
    isMenuOpen.value = false;
    router.push("/");
};

const menuItems = [
    { name: "Beranda", path: "/" },
    { name: "Fitur", path: "/features" },
    { name: "Cara Kerja", path: "/how-it-works" },
    { name: "Demo", path: "/demo" },
    { name: "Harga", path: "/pricing" },
];

const toggleMenu = () => {
    isMenuOpen.value = !isMenuOpen.value;
};

const navigateTo = (path) => {
    isMenuOpen.value = false;
    router.push(path);
};

const isActive = (path) => {
    return route.path === path;
};
</script>

<template>
    <nav
        class="fixed top-0 left-0 right-0 z-50 bg-[#1a1625] border-b border-gray-800"
    >
        <div class="max-w-7xl mx-auto px-6">
            <div class="flex justify-between items-center h-16">
                <!-- Logo -->
                <button @click="navigateTo('/')" class="flex items-center gap-3 group focus:outline-none">
                <div
                        class="w-10 h-10 bg-[#4D41C0] rounded-full flex items-center justify-center group-hover:shadow-[0_0_15px_rgba(77,65,192,0.5)] transition-all duration-300"
                    >
                        <img
                            src="../assets/LOGO.svg"
                            alt="FireVision Logo"
                            class="w-6 h-6 object-contain"
                        />
                    </div>
                    <span class="text-xl font-semibold text-white group-hover:text-[#4D41C0] transition-colors"
                        >FireVision</span
                    >
                </button>

                <!-- Desktop Menu -->
                <div class="hidden md:flex items-center gap-8">
                    <button
                        v-for="item in menuItems"
                        :key="item.name"
                        @click="navigateTo(item.path)"
                        class="text-gray-300 hover:text-[#4D41C0] font-medium transition-colors duration-200 relative group py-2"
                        :class="{ 'text-[#4D41C0] active-nav-item': isActive(item.path) }"
                    >
                        {{ item.name }}
                        <span 
                            class="absolute bottom-0 left-0 w-0 h-0.5 bg-[#4D41C0] transition-all duration-300 group-hover:w-full"
                            :class="{ 'w-full': isActive(item.path) }"
                        ></span>
                    </button>
                    
                </div>

                <!-- Auth Buttons (Guest) -->
                <div v-if="!user" class="hidden md:flex items-center gap-4">
                    <button
                        @click="navigateTo('/login')"
                        class="text-gray-300 hover:text-white px-6 py-2 font-medium transition-all duration-200 hover:bg-[#4D41C0]/10 hover:scale-105 rounded-lg"
                    >
                        Masuk
                    </button>
                    <button
                        @click="navigateTo('/register')"
                        class="bg-[#4D41C0] hover:bg-[#5D51D0] text-white px-6 py-2 rounded-lg font-semibold transition-all duration-200 shadow-lg hover:shadow-[#4D41C0]/50"
                    >
                        Daftar
                    </button>
                </div>

                <!-- User Menu (Logged In) -->
                <div v-else class="hidden md:flex items-center gap-4 border-l border-gray-700 pl-6">
                    <div class="flex flex-col items-end mr-2">
                        <span class="text-sm font-semibold text-white leading-tight">{{ getDisplayName(user.username) }}</span>
                        <span class="text-xs text-green-400">Online</span>
                    </div>
                    
                    <button @click="navigateTo('/profile')" class="w-10 h-10 rounded-full bg-[#2A2A35] border border-gray-600 flex items-center justify-center hover:border-[#6C4DFF] transition-all overflow-hidden group">
                        <span class="font-bold text-[#6C4DFF] group-hover:scale-110 transition-transform">{{ user.username.charAt(0).toUpperCase() }}</span>
                    </button>
                </div>

                <!-- Mobile Menu Button -->
                <button
                    @click="toggleMenu"
                    class="md:hidden text-gray-300 hover:text-white focus:outline-none"
                >
                    <svg
                        class="w-6 h-6"
                        fill="none"
                        stroke="currentColor"
                        viewBox="0 0 24 24"
                    >
                        <path
                            v-if="!isMenuOpen"
                            stroke-linecap="round"
                            stroke-linejoin="round"
                            stroke-width="2"
                            d="M4 6h16M4 12h16M4 18h16"
                        />
                        <path
                            v-else
                            stroke-linecap="round"
                            stroke-linejoin="round"
                            stroke-width="2"
                            d="M6 18L18 6M6 6l12 12"
                        />
                    </svg>
                </button>
            </div>

            <!-- Mobile Menu -->
            <div
                v-show="isMenuOpen"
                class="md:hidden pb-4 space-y-2 border-t border-gray-800 pt-4"
            >
                <button
                    v-for="item in menuItems"
                    :key="item.name"
                    @click="navigateTo(item.path)"
                    class="block w-full text-left px-4 py-2 text-gray-300 hover:text-[#4D41C0] hover:bg-[#4D41C0]/10 rounded-lg transition-colors duration-200"
                    :class="{ 'text-[#4D41C0] bg-[#4D41C0]/10': isActive(item.path) }"
                >
                    {{ item.name }}
                </button>
                
                <div v-if="!user" class="pt-4 space-y-2">
                    <button
                        @click="navigateTo('/login')"
                        class="block w-full text-center text-gray-300 hover:text-white px-4 py-2 rounded-lg font-medium transition-all duration-200 border border-gray-700 hover:border-[#4D41C0] hover:bg-[#4D41C0]/10 hover:scale-105"
                    >
                        Masuk
                    </button>
                    <button
                        @click="navigateTo('/register')"
                        class="block w-full text-center bg-[#4D41C0] hover:bg-[#5D51D0] text-white px-4 py-2 rounded-lg font-semibold transition-all duration-200"
                    >
                        Daftar
                    </button>
                </div>

                <div v-else class="pt-4 border-t border-gray-800 mt-2">
                     <div class="px-4 py-2 mb-2 flex items-center gap-3">
                        <div class="w-8 h-8 rounded-full bg-[#2A2A35] flex items-center justify-center border border-gray-600">
                             <span class="font-bold text-[#6C4DFF] text-xs">{{ user.username.charAt(0).toUpperCase() }}</span>
                        </div>
                        <span class="text-white font-medium">{{ getDisplayName(user.username) }}</span>
                     </div>
                     <button
                        @click="navigateTo('/profile')"
                        class="block w-full text-left px-4 py-2 text-gray-300 hover:text-[#4D41C0] hover:bg-[#4D41C0]/10 rounded-lg transition-colors"
                    >
                        Profil Saya
                    </button>
                    <button
                        @click="handleLogout"
                        class="block w-full text-left px-4 py-2 text-red-500 hover:bg-red-500/10 rounded-lg transition-colors"
                    >
                        Keluar
                    </button>
                </div>

            </div>
        </div>
    </nav>
</template>

<style scoped>
/* Active link styling for desktop */
.active-nav-item span {
    width: 100% !important;
}
</style>
