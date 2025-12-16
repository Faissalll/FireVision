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

// Footer Pages - Company
import About from "../pages/About.vue";
import Blog from "../pages/Blog.vue";
import Careers from "../pages/Careers.vue";
import Contact from "../pages/Contact.vue";

// Footer Pages - Resources
import Documentation from "../pages/Documentation.vue";
import ApiReference from "../pages/ApiReference.vue";
import Support from "../pages/Support.vue";
import Community from "../pages/Community.vue";

// Footer Pages - Legal
import Privacy from "../pages/Privacy.vue";
import Terms from "../pages/Terms.vue";
import Security from "../pages/Security.vue";
import Compliance from "../pages/Compliance.vue";

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
    { path: "/forgot-password", name: "ForgotPassword", component: () => import("../pages/ForgotPassword.vue") },
    { path: "/reset-password", name: "ResetPassword", component: () => import("../pages/ResetPassword.vue") },
    { path: "/profile", name: "Profile", component: Profile },

    // Footer Routes
    { path: "/about", name: "About", component: About },
    { path: "/blog", name: "Blog", component: Blog },
    { path: "/careers", name: "Careers", component: Careers },
    { path: "/contact", name: "Contact", component: Contact },

    { path: "/documentation", name: "Documentation", component: Documentation },
    { path: "/api-reference", name: "ApiReference", component: ApiReference },
    { path: "/support", name: "Support", component: Support },
    { path: "/community", name: "Community", component: Community },

    { path: "/privacy", name: "Privacy", component: Privacy },
    { path: "/terms", name: "Terms", component: Terms },
    { path: "/security", name: "Security", component: Security },
    { path: "/compliance", name: "Compliance", component: Compliance },
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
