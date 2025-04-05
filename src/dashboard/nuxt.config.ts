// https://nuxt.com/docs/api/configuration/nuxt-config
export default defineNuxtConfig({
    app: {
        head: {
            title: 'Weather',
        },
    },
    runtimeConfig: {
        public: {
            apiBase: process.env.NUXT_PUBLIC_API_BASE
        }
    },
    ssr: false,
    devtools: { enabled: true },
    pages: true,
    modules: ['@nuxt/ui'],
});
