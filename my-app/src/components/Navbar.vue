<script setup>
import { ref } from "vue";

const isMenuOpen = ref(false);

const menuItems = [
    { name: "Home", path: "/" },
    { name: "Features", path: "/features" },
    { name: "How It Works", path: "/how-it-works" },
    { name: "Demo", path: "/demo" },
    { name: "Pricing", path: "/pricing" },
];

const toggleMenu = () => {
    isMenuOpen.value = !isMenuOpen.value;
};
</script>

<template>
    <nav
        class="fixed top-0 left-0 right-0 z-50 bg-[#1a1625] border-b border-gray-800"
    >
        <div class="max-w-7xl mx-auto px-6">
            <div class="flex justify-between items-center h-16">
                <div class="flex items-center gap-3">
                    <div
                        class="w-10 h-10 bg-[#4D41C0] rounded-lg flex items-center justify-center p-1"
                    >
                        <img
                            src="../assets/LogoWeb.png"
                            alt="FireVision Logo"
                            class="w-full h-full object-contain"
                        />
                    </div>
                    <span class="text-xl font-semibold text-white"
                        >FireVision</span
                    >
                </div>

                <div class="hidden md:flex items-center gap-8">
                    <a
                        v-for="item in menuItems"
                        :key="item.name"
                        :href="item.path"
                        class="text-gray-300 hover:text-[#4D41C0] font-medium transition-colors duration-200 relative group"
                    >
                        {{ item.name }}
                        <span
                            class="absolute bottom-[-8px] left-0 w-0 h-0.5 bg-[#4D41C0] group-hover:w-full transition-all duration-200"
                        ></span>
                    </a>
                </div>

                <div class="hidden md:flex items-center gap-4">
                    <button
                        class="text-gray-300 hover:text-white px-6 py-2 font-medium transition-all duration-200 hover:bg-[#4D41C0]/10 hover:scale-105 rounded-lg"
                    >
                        Sign In
                    </button>
                    <button
                        class="bg-[#4D41C0] hover:bg-[#5D51D0] text-white px-6 py-2 rounded-lg font-semibold transition-all duration-200 shadow-lg hover:shadow-[#4D41C0]/50"
                    >
                        Get Started
                    </button>
                </div>

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

            <div
                v-show="isMenuOpen"
                class="md:hidden pb-4 space-y-2 border-t border-gray-800 pt-4"
            >
                <a
                    v-for="item in menuItems"
                    :key="item.name"
                    :href="item.path"
                    class="block px-4 py-2 text-gray-300 hover:text-[#4D41C0] hover:bg-[#4D41C0]/10 rounded-lg transition-colors duration-200"
                    @click="isMenuOpen = false"
                >
                    {{ item.name }}
                </a>
                <div class="pt-4 space-y-2">
                    <button
                        class="w-full text-gray-300 hover:text-white px-4 py-2 rounded-lg font-medium transition-all duration-200 border border-gray-700 hover:border-[#4D41C0] hover:bg-[#4D41C0]/10 hover:scale-105"
                    >
                        Sign In
                    </button>
                    <button
                        class="w-full bg-[#4D41C0] hover:bg-[#5D51D0] text-white px-4 py-2 rounded-lg font-semibold transition-all duration-200"
                    >
                        Get Started
                    </button>
                </div>
            </div>
        </div>
    </nav>
</template>
