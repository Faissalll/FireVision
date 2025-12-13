<script setup>
defineProps({
  isOpen: Boolean,
  title: String,
  message: String,
  buttonText: {
    type: String,
    default: "Mengerti"
  }
});

defineEmits(['close']);
</script>

<template>
  <div v-if="isOpen" class="fixed inset-0 z-50 flex items-center justify-center p-4">
    <!-- Backdrop -->
    <div 
      class="absolute inset-0 bg-black/60 backdrop-blur-sm transition-opacity" 
      @click="$emit('close')"
    ></div>

    <!-- Modal Content -->
    <div class="relative bg-[#1a1a2e] border border-[#2d2d48] rounded-2xl p-6 max-w-sm w-full shadow-2xl transform transition-all scale-100 ring-1 ring-white/10">
      <div class="text-center">
        <!-- Icon -->
        <div class="mx-auto flex items-center justify-center h-12 w-12 rounded-full bg-[#2d2d48] mb-4">
          <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6 text-[#8b5cf6]" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
          </svg>
        </div>
        
        <h3 class="text-lg leading-6 font-bold text-white mb-2">{{ title }}</h3>
        
        <div class="mt-2">
          <p class="text-sm text-gray-300">
            {{ message }}
          </p>
        </div>
      </div>

      <div class="mt-6 flex justify-center">
        <button
          type="button"
          class="inline-flex justify-center px-6 py-2 text-sm font-semibold text-white bg-[#8b5cf6] hover:bg-[#7c3aed] border border-transparent rounded-full focus:outline-none focus-visible:ring-2 focus-visible:ring-offset-2 focus-visible:ring-purple-500 transition-colors shadow-lg shadow-purple-500/20"
          @click="$emit('close')"
        >
          {{ buttonText }}
        </button>
      </div>
    </div>
  </div>
</template>
