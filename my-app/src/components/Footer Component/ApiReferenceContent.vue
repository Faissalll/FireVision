<template>
    <div class="flex-grow pt-24 pb-12 px-4 sm:px-6 lg:px-8 max-w-5xl mx-auto w-full">
        <button @click="$router.back()" class="flex items-center gap-2 text-gray-400 hover:text-white mb-8 transition-colors group">
            <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="group-hover:-translate-x-1 transition-transform"><path d="m15 18-6-6 6-6"/></svg>
            Kembali
        </button>
        <h1 class="text-4xl font-bold mb-2 bg-gradient-to-r from-white to-gray-400 bg-clip-text text-transparent">FireVision API Reference</h1>
        <p class="text-gray-400 mb-10">Versi 1.0.0 • Base URL: <code class="bg-gray-800 px-2 py-1 rounded text-[#6C4DFF]">{{ apiBaseUrl }}/api</code></p>
        
        <div class="space-y-8">
            <!-- Endpoint 1 -->
            <div class="border border-gray-800 rounded-xl overflow-hidden">
                <div class="bg-[#1A1A2E] px-6 py-4 border-b border-gray-800 flex items-center gap-4">
                    <span class="bg-green-500/20 text-green-400 px-3 py-1 rounded font-bold text-sm">POST</span>
                    <code class="text-gray-300 font-mono">/start-detection</code>
                </div>
                <div class="p-6">
                    <p class="text-gray-400 mb-4">Memulai sesi deteksi baru untuk kamera tertentu.</p>
                    <h3 class="text-white font-semibold mb-2">Parameters</h3>
                    <pre class="bg-gray-900 p-4 rounded-lg text-sm text-gray-300 overflow-x-auto">
{
"username": "string (required)",
"camera_source": "WEBCAM | IP_CAMERA",
"ip_camera_url": "string (optional)",
"sensitivity": "number (0-100)"
}</pre>
                </div>
            </div>

            <!-- Endpoint 2 -->
            <div class="border border-gray-800 rounded-xl overflow-hidden">
                <div class="bg-[#1A1A2E] px-6 py-4 border-b border-gray-800 flex items-center gap-4">
                    <span class="bg-blue-500/20 text-blue-400 px-3 py-1 rounded font-bold text-sm">GET</span>
                    <code class="text-gray-300 font-mono">/detections</code>
                </div>
                <div class="p-6">
                    <p class="text-gray-400 mb-4">Mengambil data bounding box deteksi real-time untuk dirender di frontend.</p>
                    <h3 class="text-white font-semibold mb-2">Query Params</h3>
                    <ul class="list-disc list-inside text-gray-400 text-sm">
                        <li><code class="text-gray-300">session</code>: Session ID yang dikembalikan dari start-detection.</li>
                    </ul>
                </div>
            </div>

            <!-- Endpoint 3 -->
            <div class="border border-gray-800 rounded-xl overflow-hidden">
                <div class="bg-[#1A1A2E] px-6 py-4 border-b border-gray-800 flex items-center gap-4">
                    <span class="bg-red-500/20 text-red-400 px-3 py-1 rounded font-bold text-sm">POST</span>
                    <code class="text-gray-300 font-mono">/stop-detection</code>
                </div>
                <div class="p-6">
                    <p class="text-gray-400 mb-4">Menghentikan sesi deteksi dan mematikan kamera.</p>
                </div>
            </div>
        </div>
    </div>
</template>
