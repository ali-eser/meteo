<script setup lang="ts">
    import type { ForecastObj } from '~/types';
    import type { PropType } from 'vue';

    // define props to be passed in
    const props = defineProps({
        // determine if the sidebar is open or not
        isSidebarOpen: {
            type: Boolean,
            default: false
        },
        isSidebarLoading: {
            type: Boolean,
            default:false
        },
        // store seven day forecast data
        forecastData: {
            type: [Object, null] as PropType<ForecastObj | null>,
            default: null
        }
    });

    watch(() => props.forecastData, (newValue, _oldValue) => {
        if (newValue !== null) {
            emit("update:isSidebarLoading", false);
        }
    });

    // close sidebar and flush forecastData state on close button click
    const flush = () => {
        emit('update:isSidebarOpen', false);

        // wait until sidebar transition is complete,
        // otherwise the data would disappear before the sidebar closes
        setTimeout(() => {
            emit('update:forecastData', null);
        }, 300);
    }

    // define emits to update values of isSidebarOpen and forecastData states
    const emit = defineEmits(["update:isSidebarOpen", "update:forecastData", "update:isSidebarLoading"]);
</script>

<template>
    <div>
        <USlideover class="backdrop-brightness-50"  v-model="props.isSidebarOpen" :overlay="false">

            <!-- show a loading indicator until the data is loaded -->
            <UProgress
                v-if="props.isSidebarLoading"
                :ui="{ progress: { rounded: 'rounded-none' } }"
                animation="carousel-inverse"
            />

            <!-- only show card if forecastData is not null -->
            <UCard
                v-if="props.forecastData"
                class="flex flex-col overflow-auto h-full"
                :ui="{ rounded: 'rounded-none', shadow: 'shadow', background: 'dark:bg-neutral-900' }"
            >
                <template #header>
                    <div class="flex justify-between items-center h-fit">
                        <div class="flex-col justify-between">
                            <h3 class="text-2xl font-semibold">{{ props.forecastData.name }}, {{ props.forecastData.country }}</h3>
                            <p class="text-gray-400 text-sm mt-6">This Week</p>
                        </div>

                        <!-- show a close button for closing the sidebar -->
                        <UButton
                            class="justify-end"
                            icon="i-heroicons-x-mark-20-solid"
                            color="gray"
                            variant="solid"
                            size="2xs"
                            @click="flush"
                            :ui="{ icon: { color: 'white' } }"
                        />
                    </div>
                </template>
                <div class="flex-col px-0.5 -mt-7 items-center">

                    <!-- show a card component for each day data -->
                    <UCard class="mb-5 h-24 flex items-center" v-for="(time, index) in props.forecastData.daily.time" :key="index"
                        :ui="{ rounded: 'rounded-2xl', background: 'bg-gray-100 dark:bg-gray-400/20' }"
                    >
                        <div class="flex justify-between w-80 items-center">
                            <div class="space-x-3 flex items-center">

                                <!-- show a weather icon corresponding to the mapped weather code -->
                                <img
                                    :src="`/icons/${props.forecastData.daily.weather_code[index]}.svg`"
                                    :alt="`weather icon ${props.forecastData.daily.weather_code[index]}`"
                                />
                                <span class="font-medium text-3xl">{{ new Date(time).toLocaleDateString('en-US', { weekday: 'long' }) }}</span>
                            </div>

                            <!-- format min-max temperature and rain data -->
                            <div class="flex-col items-center w-20 space-y-1">
                                <div class="flex justify-between w-28">
                                    <p class="text-gray-500">Min. </p>
                                    {{ props.forecastData.daily.temperature_2m_min[index] }}°C
                                </div>
                                <div class="flex justify-between w-28">
                                    <p class="text-gray-500">Max. </p>
                                    {{ props.forecastData.daily.temperature_2m_max[index] }}°C
                                </div>
                                <div class="flex justify-between w-28">
                                    <p class="text-gray-500">Rain: </p>
                                    {{ props.forecastData.daily.rain_sum[index] }} mm
                                </div>
                            </div>
                        </div>
                    </UCard>
                </div>
            </UCard>
        </USlideover>
    </div>
</template>
