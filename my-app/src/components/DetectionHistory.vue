<script setup>
import { ref, onMounted, onUnmounted, computed } from "vue";

// Data
const historyData = ref([]);
const isLoading = ref(true);

// Filters
const selectedDateStart = ref("");
const selectedDateEnd = ref("");
const selectedCamera = ref("All");
const selectedStatus = ref("Semua");

// Pagination
const currentPage = ref(1);
const itemsPerPage = 8;

// Fetch Data from Backend
const fetchHistory = async () => {
    try {
        const response = await fetch(`${import.meta.env.VITE_API_BASE_URL}/api/history`);
        if (!response.ok) throw new Error("Gagal mengambil data");
        const data = await response.json();
        historyData.value = data;
        isLoading.value = false;
    } catch (error) {
        console.error("Error fetching history:", error);
        isLoading.value = false;
    }
};

// Update Status Logic
const updateStatus = async (item, newStatus) => {
    try {
        const response = await fetch(`${import.meta.env.VITE_API_BASE_URL}/api/history/update-status`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ db_id: item.db_id, status: newStatus })
        });
        if (response.ok) {
            // Update local state immediately for better UX
            item.status = newStatus;
        }
    } catch (error) {
        console.error("Error updating status:", error);
    }
};

// Auto Refresh
let pollingInterval;
onMounted(() => {
    fetchHistory();
    pollingInterval = setInterval(fetchHistory, 5000); // Polling every 5s
});

onUnmounted(() => {
    clearInterval(pollingInterval);
});

// Computed Logic for Filtering & Stats
const filteredData = computed(() => {
    return historyData.value.filter(item => {
        const matchStatus = selectedStatus.value === "Semua" || item.status === selectedStatus.value;
        const matchCamera = selectedCamera.value === "All" || item.camera.includes(selectedCamera.value);
        
        let matchDate = true;
        if(selectedDateStart.value && selectedDateEnd.value) {
            matchDate = item.date >= selectedDateStart.value && item.date <= selectedDateEnd.value;
        }

        return matchStatus && matchCamera && matchDate;
    });
});

const totalPages = computed(() => Math.ceil(filteredData.value.length / itemsPerPage));

const paginatedData = computed(() => {
    const start = (currentPage.value - 1) * itemsPerPage;
    const end = start + itemsPerPage;
    return filteredData.value.slice(start, end);
});

const stats = computed(() => {
    const today = new Date().toISOString().split('T')[0];
    const todaysAlarms = historyData.value.filter(d => d.date === today);
    return {
        today: todaysAlarms.length,
        completed: todaysAlarms.filter(d => d.status === 'Selesai').length,
        falseAlarm: todaysAlarms.filter(d => d.status === 'False Alarm').length
    };
});

const getStatusColor = (status) => {
    switch (status) {
        case "Baru": return "bg-purple-600 text-white";
        case "Selesai": return "bg-green-600 text-white";
        case "False Alarm": return "bg-orange-500 text-white";
        default: return "bg-gray-600 text-white";
    }
};

// Dropdown State for Actions
const activeDropdown = ref(null);
const toggleAction = (id) => {
    if (activeDropdown.value === id) {
        activeDropdown.value = null;
    } else {
        activeDropdown.value = id;
    }
};
</script>

<template>
    <div class="grid grid-cols-1 lg:grid-cols-4 gap-6">
        
        <!-- Left Content (Filter & Table) -->
        <div class="lg:col-span-3 space-y-6">
            
            <!-- Filter Card -->
            <div class="bg-[#0B0F1A] p-6 rounded-2xl shadow-lg border border-gray-800/50 backdrop-blur-sm animate-fade-in-up">
                <div class="flex flex-col md:flex-row gap-4 items-end">
                    
                    <!-- Date Range -->
                    <div class="flex-1 w-full md:w-auto">
                        <label class="block text-sm font-medium text-gray-400 mb-2">Rentang Tanggal</label>
                        <div class="flex gap-2 items-center">
                            <input type="date" v-model="selectedDateStart" class="bg-[#1A1F2E] border border-gray-700 rounded-lg px-3 py-2 text-sm focus:outline-none focus:border-[#6C4DFF] w-full" placeholder="Dari">
                            <span class="text-gray-500">-</span>
                            <input type="date" v-model="selectedDateEnd" class="bg-[#1A1F2E] border border-gray-700 rounded-lg px-3 py-2 text-sm focus:outline-none focus:border-[#6C4DFF] w-full" placeholder="Sampai">
                        </div>
                    </div>

                    <!-- Camera Dropdown -->
                    <div class="flex-1 w-full md:w-auto">
                        <label class="block text-sm font-medium text-gray-400 mb-2">Kamera</label>
                        <select v-model="selectedCamera" class="w-full bg-[#1A1F2E] border border-gray-700 rounded-lg px-3 py-2 text-sm focus:outline-none focus:border-[#6C4DFF]">
                            <option value="All">Semua Kamera</option>
                            <option value="Kamera 1">Kamera 1</option>
                            <option value="Kamera Gudang">Kamera Gudang</option>
                            <option value="Kamera Parkir">Kamera Parkir</option>
                            <option value="Kamera Lobi">Kamera Lobi</option>
                        </select>
                    </div>

                    <!-- Status Dropdown -->
                    <div class="flex-1 w-full md:w-auto">
                        <label class="block text-sm font-medium text-gray-400 mb-2">Status</label>
                        <select v-model="selectedStatus" class="w-full bg-[#1A1F2E] border border-gray-700 rounded-lg px-3 py-2 text-sm focus:outline-none focus:border-[#6C4DFF]">
                            <option value="Semua">Semua Status</option>
                            <option value="Baru">Baru</option>
                            <option value="Selesai">Selesai</option>
                            <option value="False Alarm">False Alarm</option>
                        </select>
                    </div>

                    <!-- Buttons -->
                    <div class="flex gap-3 mt-4 md:mt-0 w-full md:w-auto">
                        <button class="flex-1 md:flex-none px-5 py-2 bg-[#6C4DFF] hover:bg-[#5839EE] text-white text-sm font-semibold rounded-lg transition-colors shadow-lg shadow-[#6C4DFF]/30">
                            Terapkan
                        </button>
                        <button class="flex-1 md:flex-none px-5 py-2 bg-transparent border border-gray-600 hover:bg-gray-800 text-gray-300 text-sm font-semibold rounded-lg transition-colors">
                            Reset
                        </button>
                    </div>
                </div>
            </div>

            <!-- Table Card -->
            <div class="bg-[#0B0F1A] rounded-2xl shadow-lg border border-gray-800/50 overflow-hidden animate-fade-in-up" style="animation-delay: 0.1s;">
                <div class="overflow-x-auto">
                    <table class="w-full text-left border-collapse">
                        <thead>
                            <tr class="bg-[#151926] text-gray-400 text-sm uppercase tracking-wider border-b border-gray-800">
                                <th class="p-4 font-semibold">ID Alarm</th>
                                <th class="p-4 font-semibold">Waktu</th>
                                <th class="p-4 font-semibold">Kamera</th>
                                <th class="p-4 font-semibold">Zona</th>
                                <th class="p-4 font-semibold">Confidence</th>
                                <th class="p-4 font-semibold">Status</th>
                                <th class="p-4 font-semibold text-center">Aksi</th>
                            </tr>
                        </thead>
                        <tbody class="divide-y divide-gray-800">
                            <tr v-if="historyData.length === 0 && !isLoading">
                                <td colspan="7" class="p-8 text-center text-gray-500">Belum ada data riwayat deteksi.</td>
                            </tr>
                            <tr v-for="item in paginatedData" :key="item.id" class="hover:bg-[#1A1F2E]/50 transition-colors group">
                                <td class="p-4 font-medium text-white group-hover:text-[#6C4DFF] transition-colors">{{ item.id }}</td>
                                <td class="p-4 text-gray-300">
                                    <div class="flex flex-col">
                                        <span>{{ item.time }}</span>
                                        <span class="text-xs text-gray-500">{{ item.date }}</span>
                                    </div>
                                </td>
                                <td class="p-4 text-gray-300">{{ item.camera }}</td>
                                <td class="p-4 text-gray-300">{{ item.zone }}</td>
                                <td class="p-4 text-gray-300">
                                    <div class="flex items-center gap-2">
                                        <div class="w-16 h-2 bg-gray-700 rounded-full overflow-hidden">
                                            <div class="h-full bg-gradient-to-r from-blue-500 to-[#6C4DFF]" :style="{ width: item.confidence + '%' }"></div>
                                        </div>
                                        <span class="text-xs font-semibold">{{ item.confidence }}%</span>
                                    </div>
                                </td>
                                <td class="p-4">
                                    <span :class="['px-3 py-1 rounded-full text-xs font-semibold shadow-sm', getStatusColor(item.status)]">
                                        {{ item.status }}
                                    </span>
                                </td>
                                <td class="p-4 text-center relative">
                                    <button @click="toggleAction(item.id)" class="text-gray-400 hover:text-white p-2 rounded-lg hover:bg-gray-700/50 transition-colors" title="Aksi">
                                        <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="1"/><circle cx="19" cy="12" r="1"/><circle cx="5" cy="12" r="1"/></svg>
                                    </button>

                                    <!-- Dropdown Aksi -->
                                    <div v-if="activeDropdown === item.id" class="absolute right-8 top-8 w-40 bg-[#0B0F1A] border border-gray-800 rounded-lg shadow-xl z-10 overflow-hidden text-left" @mouseleave="activeDropdown = null">
                                        <button @click="updateStatus(item, 'Selesai'); activeDropdown = null" class="w-full px-4 py-2 text-xs text-green-400 hover:bg-gray-800 flex items-center gap-2">
                                            <svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="20 6 9 17 4 12"/></svg>
                                            Tandai Selesai
                                        </button>
                                        <button @click="updateStatus(item, 'False Alarm'); activeDropdown = null" class="w-full px-4 py-2 text-xs text-orange-400 hover:bg-gray-800 flex items-center gap-2">
                                            <svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M10.29 3.86L1.82 18a2 2 0 0 0 1.71 3h16.94a2 2 0 0 0 1.71-3L13.71 3.86a2 2 0 0 0-3.42 0z"/><line x1="12" y1="9" x2="12" y2="13"/><line x1="12" y1="17" x2="12.01" y2="17"/></svg>
                                            False Alarm
                                        </button>
                                    </div>
                                </td>
                            </tr>
                        </tbody>
                    </table>
                </div>

                <!-- Pagination -->
                <div class="p-4 border-t border-gray-800 flex flex-col sm:flex-row justify-between items-center gap-4 bg-[#0B0F1A]">
                    <span class="text-sm text-gray-400">
                        Menampilkan 
                        <span class="text-white font-medium">{{ filteredData.length > 0 ? (currentPage - 1) * itemsPerPage + 1 : 0 }}–{{ Math.min(currentPage * itemsPerPage, filteredData.length) }}</span> 
                        dari 
                        <span class="text-white font-medium">{{ filteredData.length }}</span> 
                        alarm
                    </span>
                    
                    <div class="flex items-center gap-2">
                        <button class="px-3 py-1 bg-[#1A1F2E] hover:bg-gray-700 text-gray-300 rounded text-sm disabled:opacity-50 disabled:cursor-not-allowed" :disabled="currentPage === 1">
                            Previous
                        </button>
                        <div class="flex gap-1">
                            <button v-for="i in 3" :key="i" :class="['w-8 h-8 rounded text-sm font-medium flex items-center justify-center transition-colors', currentPage === i ? 'bg-[#6C4DFF] text-white shadow-lg shadow-[#6C4DFF]/25' : 'bg-[#1A1F2E] text-gray-400 hover:bg-gray-700 hover:text-white']">
                                {{ i }}
                            </button>
                            <span class="px-2 text-gray-500">...</span>
                            <button class="w-8 h-8 rounded text-sm font-medium flex items-center justify-center bg-[#1A1F2E] text-gray-400 hover:bg-gray-700 hover:text-white transition-colors">
                                {{ totalPages }}
                            </button>
                        </div>
                        <button class="px-3 py-1 bg-[#1A1F2E] hover:bg-gray-700 text-gray-300 rounded text-sm">
                            Next
                        </button>
                    </div>
                </div>
            </div>

        </div>

        <!-- Right Sidebar (Stats) -->
        <div class="lg:col-span-1 space-y-6">
            
            <div class="bg-[#0B0F1A] p-6 rounded-2xl shadow-lg border border-gray-800/50 sticky top-24 animate-fade-in-up" style="animation-delay: 0.2s;">
                <h3 class="text-lg font-bold mb-6 flex items-center gap-2">
                    <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#6C4DFF" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M3 3v18h18"/><path d="M18 17V9"/><path d="M13 17V5"/><path d="M8 17v-3"/></svg>
                    Ringkasan Hari Ini
                </h3>

                <div class="space-y-4">
                    <!-- Helper Components for Stats Row -->
                    <div class="flex items-center justify-between p-4 bg-[#151926] rounded-xl border border-gray-800 hover:border-[#6C4DFF]/30 transition-colors">
                        <div>
                            <p class="text-gray-400 text-sm mb-1">Total Alarm</p>
                            <p class="text-2xl font-bold">{{ stats.today }}</p>
                        </div>
                        <div class="p-2 bg-[#6C4DFF]/10 text-[#6C4DFF] rounded-lg">
                            <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M6 9H4.5a2.5 2.5 0 0 1 0-5H6"/><path d="M18 9h1.5a2.5 2.5 0 0 0 0-5H18"/><path d="M4 22h16"/><path d="M10 14.66V17c0 .55-.47.98-.97 1.21C7.85 18.75 7 20.24 7 22"/><path d="M14 14.66V17c0 .55.47.98.97 1.21C16.15 18.75 17 20.24 17 22"/><path d="M18 2H6v7a6 6 0 0 0 12 0V2Z"/></svg>
                        </div>
                    </div>

                    <div class="flex items-center justify-between p-4 bg-[#151926] rounded-xl border border-gray-800 hover:border-green-500/30 transition-colors">
                        <div>
                            <p class="text-gray-400 text-sm mb-1">Selesai</p>
                            <p class="text-2xl font-bold text-green-400">{{ stats.completed }}</p>
                        </div>
                        <div class="p-2 bg-green-500/10 text-green-500 rounded-lg">
                            <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"/><polyline points="22 4 12 14.01 9 11.01"/></svg>
                        </div>
                    </div>

                    <div class="flex items-center justify-between p-4 bg-[#151926] rounded-xl border border-gray-800 hover:border-orange-500/30 transition-colors">
                        <div>
                            <p class="text-gray-400 text-sm mb-1">False Alarm</p>
                            <p class="text-2xl font-bold text-orange-400">{{ stats.falseAlarm }}</p>
                        </div>
                        <div class="p-2 bg-orange-500/10 text-orange-500 rounded-lg">
                            <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M10.29 3.86L1.82 18a2 2 0 0 0 1.71 3h16.94a2 2 0 0 0 1.71-3L13.71 3.86a2 2 0 0 0-3.42 0z"/><line x1="12" y1="9" x2="12" y2="13"/><line x1="12" y1="17" x2="12.01" y2="17"/></svg>
                        </div>
                    </div>
                </div>
            </div>

        </div>

    </div>
</template>

<style scoped>
@keyframes fadeInUp {
    from {
        opacity: 0;
        transform: translateY(20px);
    }
    to {
        opacity: 1;
        transform: translateY(0);
    }
}

.animate-fade-in-up {
    animation: fadeInUp 0.6s ease-out forwards;
    opacity: 0; 
}
</style>
