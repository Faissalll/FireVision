<template>
    <div class="bg-[#0F0F1E] py-20 px-4">
        <div class="max-w-7xl mx-auto">
            <div class="text-center mb-16">
                <h2 class="text-4xl md:text-5xl font-bold text-white mb-4">
                    How It Works
                </h2>
                <p class="text-xl text-gray-400">
                    Three simple steps to complete fire safety protection
                </p>
            </div>

            <div class="grid grid-cols-1 md:grid-cols-3 gap-8 relative">
                <div ref="cardRefs" class="how-it-works-card relative">
                    <div
                        class="absolute -top-4 -left-4 w-14 h-14 bg-[#4D41C0] rounded-full flex items-center justify-center z-10"
                    >
                        <span class="text-white font-bold text-xl">01</span>
                    </div>

                    <div
                        class="bg-[#1A1A2E] rounded-2xl p-8 border border-[#33333C] hover:border-[#4D41C0] hover:shadow-[0_0_30px_rgba(77,65,192,0.5)] transition-all duration-300 group"
                    >
                        <div
                            class="w-24 h-24 bg-[#2A2A4E] rounded-2xl flex items-center justify-center mb-6 group-hover:shadow-[0_0_20px_rgba(77,65,192,0.6)] transition-all duration-300"
                        >
                            <svg
                                class="w-12 h-12 text-[#4D41C0]"
                                fill="none"
                                stroke="currentColor"
                                viewBox="0 0 24 24"
                            >
                                <path
                                    stroke-linecap="round"
                                    stroke-linejoin="round"
                                    stroke-width="2"
                                    d="M3 9a2 2 0 012-2h.93a2 2 0 001.664-.89l.812-1.22A2 2 0 0110.07 4h3.86a2 2 0 011.664.89l.812 1.22A2 2 0 0018.07 7H19a2 2 0 012 2v9a2 2 0 01-2 2H5a2 2 0 01-2-2V9z"
                                />
                                <path
                                    stroke-linecap="round"
                                    stroke-linejoin="round"
                                    stroke-width="2"
                                    d="M15 13a3 3 0 11-6 0 3 3 0 016 0z"
                                />
                            </svg>
                        </div>

                        <h3 class="text-2xl font-bold text-white mb-4">
                            Camera Captures
                        </h3>
                        <p class="text-gray-400 leading-relaxed">
                            High-resolution cameras continuously monitor your
                            environment in real-time
                        </p>
                    </div>

                    <div
                        class="hidden md:block absolute top-1/2 -right-4 transform -translate-y-1/2 z-20"
                    >
                        <div
                            class="w-8 h-8 bg-[#4D41C0] rounded-full flex items-center justify-center"
                        >
                            <svg
                                class="w-4 h-4 text-white"
                                fill="none"
                                stroke="currentColor"
                                viewBox="0 0 24 24"
                            >
                                <path
                                    stroke-linecap="round"
                                    stroke-linejoin="round"
                                    stroke-width="2"
                                    d="M9 5l7 7-7 7"
                                />
                            </svg>
                        </div>
                    </div>
                </div>

                <div ref="cardRefs" class="how-it-works-card relative">
                    <div
                        class="absolute -top-4 -left-4 w-14 h-14 bg-[#4D41C0] rounded-full flex items-center justify-center z-10"
                    >
                        <span class="text-white font-bold text-xl">02</span>
                    </div>

                    <div
                        class="bg-[#1A1A2E] rounded-2xl p-8 border border-[#33333C] hover:border-[#4D41C0] hover:shadow-[0_0_30px_rgba(77,65,192,0.5)] transition-all duration-300 group"
                    >
                        <div
                            class="w-24 h-24 bg-[#2A2A4E] rounded-2xl flex items-center justify-center mb-6 group-hover:shadow-[0_0_20px_rgba(77,65,192,0.6)] transition-all duration-300"
                        >
                            <svg
                                class="w-12 h-12 text-[#4D41C0]"
                                fill="none"
                                stroke="currentColor"
                                viewBox="0 0 24 24"
                            >
                                <path
                                    stroke-linecap="round"
                                    stroke-linejoin="round"
                                    stroke-width="2"
                                    d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z"
                                />
                            </svg>
                        </div>

                        <h3 class="text-2xl font-bold text-white mb-4">
                            AI Analyzes Smoke/Flame
                        </h3>
                        <p class="text-gray-400 leading-relaxed">
                            Deep learning models detect fire and smoke patterns
                            with 99.9% accuracy
                        </p>
                    </div>

                    <div
                        class="hidden md:block absolute top-1/2 -right-4 transform -translate-y-1/2 z-20"
                    >
                        <div
                            class="w-8 h-8 bg-[#4D41C0] rounded-full flex items-center justify-center"
                        >
                            <svg
                                class="w-4 h-4 text-white"
                                fill="none"
                                stroke="currentColor"
                                viewBox="0 0 24 24"
                            >
                                <path
                                    stroke-linecap="round"
                                    stroke-linejoin="round"
                                    stroke-width="2"
                                    d="M9 5l7 7-7 7"
                                />
                            </svg>
                        </div>
                    </div>
                </div>

                <div ref="cardRefs" class="how-it-works-card relative">
                    <div
                        class="absolute -top-4 -left-4 w-14 h-14 bg-[#4D41C0] rounded-full flex items-center justify-center z-10"
                    >
                        <span class="text-white font-bold text-xl">03</span>
                    </div>

                    <div
                        class="bg-[#1A1A2E] rounded-2xl p-8 border border-[#33333C] hover:border-[#4D41C0] hover:shadow-[0_0_30px_rgba(77,65,192,0.5)] transition-all duration-300 group"
                    >
                        <div
                            class="w-24 h-24 bg-[#2A2A4E] rounded-2xl flex items-center justify-center mb-6 group-hover:shadow-[0_0_20px_rgba(77,65,192,0.6)] transition-all duration-300"
                        >
                            <svg
                                class="w-12 h-12 text-[#4D41C0]"
                                fill="none"
                                stroke="currentColor"
                                viewBox="0 0 24 24"
                            >
                                <path
                                    stroke-linecap="round"
                                    stroke-linejoin="round"
                                    stroke-width="2"
                                    d="M15 17h5l-1.405-1.405A2.032 2.032 0 0118 14.158V11a6.002 6.002 0 00-4-5.659V5a2 2 0 10-4 0v.341C7.67 6.165 6 8.388 6 11v3.159c0 .538-.214 1.055-.595 1.436L4 17h5m6 0v1a3 3 0 11-6 0v-1m6 0H9"
                                />
                            </svg>
                        </div>

                        <h3 class="text-2xl font-bold text-white mb-4">
                            FireVision Sends Alert
                        </h3>
                        <p class="text-gray-400 leading-relaxed">
                            Instant notifications sent to your team via SMS,
                            email, and mobile app
                        </p>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'

const props = defineProps({
  delayAnimation: {
    type: Boolean,
    default: false
  }
})

const cardRefs = ref([])

onMounted(() => {
  const delay = props.delayAnimation ? 2000 : 0

  setTimeout(() => {
    const observer = new IntersectionObserver(
      (entries) => {
        entries.forEach((entry, index) => {
          if (entry.isIntersecting) {
            entry.target.style.animationDelay = `${index * 0.2}s`
            entry.target.classList.add('animate')
            observer.unobserve(entry.target)
          }
        })
      },
      { threshold: 0.1 }
    )

    cardRefs.value.forEach((card) => {
      if (card) observer.observe(card)
    })
  }, delay)
})
</script>

<style scoped>
.how-it-works-card {
  opacity: 0;
  transform: translateY(20px);
  animation: fadeInUp 0.6s ease-out forwards;
}

@keyframes fadeInUp {
  to {
    opacity: 1;
    transform: translateY(0);
  }
}
</style>
