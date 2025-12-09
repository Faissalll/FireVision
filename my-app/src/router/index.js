import { createRouter, createWebHistory } from "vue-router";
import Home from "../pages/Home.vue";
import Features from "../pages/Features.vue";
import HowItWorks from "../pages/HowItWorks.vue";
import Demo from "../pages/Demo.vue";
import Pricing from "../pages/Pricing.vue";
import History from "../pages/History.vue";
import NotificationSettings from "../pages/NotificationSettings.vue";

import Login from "../pages/Login.vue";
import Register from "../pages/Register.vue";
import Profile from "../pages/Profile.vue";

const routes = [
    { path: "/", name: "Home", component: Home },
    { path: "/features", name: "Features", component: Features },
    { path: "/how-it-works", name: "HowItWorks", component: HowItWorks },
    { path: "/demo", name: "Demo", component: Demo },
    { path: "/pricing", name: "Pricing", component: Pricing },
    { path: "/history", name: "History", component: History },
    { path: "/notifications", name: "NotificationSettings", component: NotificationSettings },
    { path: "/login", name: "Login", component: Login },
    { path: "/register", name: "Register", component: Register },
    { path: "/profile", name: "Profile", component: Profile },
];

const router = createRouter({
    history: createWebHistory(import.meta.env.BASE_URL),
    routes,
    scrollBehavior(to, from, savedPosition) {
        if (to.hash) {
            return { el: to.hash, behavior: "smooth" };
        }
        // Always scroll to top, even on refresh/back
        return { top: 0, left: 0 };
    },
});

export default router;
