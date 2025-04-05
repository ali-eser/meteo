export default defineAppConfig({
    ui: {
        primary: 'neutral',
        gray: 'neutral',
        // table styling
        table: {
            base: "divide-y divide-gray-300 dark:divide-gray-800-",
            thead: "bg-gray-50 dark:bg-gray-800",
            tbody: "divide-y divide-gray-200 dark:divide-gray-800 bg-gray-100 dark:bg-neutral-800/40",
            tr: {
              base: "hover:bg-gray-50 dark:hover:bg-gray-800",
              selected: "bg-primary-50 dark:bg-primary-900/20",
            },
            th: {
              base: "px-7 text-left font-semibold text-gray-900 dark:bg-gray-700/20 dark:text-white",
            },
            td: {
              base: "whitespace-nowrap w-screen px-7 text-gray-500 dark:text-slate-300",
            }
        },
        // card styling
        card: {
            divide: "divide-white dark:divide-neutral-900",
        }
    }
});
