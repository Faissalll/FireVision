<template>
    <div class="flex-grow pt-24 pb-12 px-4 sm:px-6 lg:px-8 max-w-4xl mx-auto w-full">
        <button @click="$router.back()" class="flex items-center gap-2 text-gray-400 hover:text-white mb-8 transition-colors group">
            <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="group-hover:-translate-x-1 transition-transform"><path d="m15 18-6-6 6-6"/></svg>
            Kembali
        </button>
        <h1 class="text-3xl font-bold mb-8 bg-gradient-to-r from-white to-gray-400 bg-clip-text text-transparent">Syarat dan Ketentuan</h1>
        
        <div class="prose prose-invert prose-lg max-w-none text-gray-300">
            <p>Selamat datang di FireVision.</p>
            
            <h3>1. Penerimaan Syarat</h3>
            <p>
                Dengan mengakses atau menggunakan layanan kami, Anda setuju untuk terikat oleh Syarat dan Ketentuan ini dan Kebijakan Privasi kami.
            </p>

            <h3>2. Penggunaan Layanan</h3>
            <p>
                Layanan FireVision ditujukan sebagai alat bantu deteksi dini kebakaran. Layanan ini <strong>bukan</strong> pengganti sistem pemadam kebakaran profesional atau prosedur keselamatan standar.
                Kami tidak bertanggung jawab atas kerugian fisik atau materi yang terjadi akibat kegagalan deteksi.
            </p>

            <h3>3. Akun Pengguna</h3>
            <p>
                Anda bertanggung jawab untuk menjaga kerahasiaan kata sandi akun Anda dan untuk semua aktivitas yang terjadi di bawah akun Anda.
            </p>
        </div>
    </div>
</template>
