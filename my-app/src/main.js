import { createApp } from "vue";
import App from "./App.vue";
import router from "./router";

// Prevent browser from restoring scroll position
if ('scrollRestoration' in history) {
  history.scrollRestoration = 'manual';
}

createApp(App).use(router).mount("#app");
