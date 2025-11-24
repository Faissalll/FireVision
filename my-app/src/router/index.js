import { createRouter, createWebHistory } from "vue-router";
import Home from "../pages/Home.vue";
import Features from "../pages/Features.vue";
import HowItWorks from "../pages/HowItWorks.vue";
import Demo from "../pages/Demo.vue";
import Pricing from "../pages/Pricing.vue";

const routes = [
    { path: "/", name: "Home", component: Home },
    { path: "/features", name: "Features", component: Features },
    { path: "/how-it-works", name: "HowItWorks", component: HowItWorks },
    { path: "/demo", name: "Demo", component: Demo },
    { path: "/pricing", name: "Pricing", component: Pricing },
];

const router = createRouter({
    history: createWebHistory(import.meta.env.BASE_URL),
    routes,
    scrollBehavior(to, from, savedPosition) {
        if (savedPosition) return savedPosition;
        if (to.hash) {
            return { el: to.hash, behavior: "smooth" };
        }
        return { top: 0, behavior: "smooth" };
    },
});

export default router;
