<script setup lang="ts">
    import type { WeatherObj, ForecastObj, LocationCoords } from '~/types';
    import { getCurrentCoords } from '~/utils';

    // import useWeatherApi composable
    const { getAllWeatherData, getForecastData, getSingleWeatherData } = useWeatherApi();

    // store locations fetched from the database
    const locations = ref<WeatherObj[]>([]);

    // determine if the app should fetch forecast of a city
    const shouldGetForecast = ref<number | null>(null);

    // store seven day forecast data
    const forecastData = ref<ForecastObj | null>(null);

    // determine whether or not the location add modal is shown
    const isModalOpen = ref<boolean>(false);

    // determine whether or not the sidebar is shown and if its loading data
    const isSidebarOpen = ref<boolean>(false);
    const isSidebarLoading = ref<boolean>(false);

    // show a loading icon if the table is loading the data
    const isTableLoading = ref<boolean>(false);

    // store current weather if location access allowed by the user
    const currentWeather = ref<string | null>(null);

    // set locations state on component mount
    onMounted(async () => {
        isTableLoading.value = true;
        locations.value = await getAllWeatherData();
        isTableLoading.value = false;

        // fetch current location's temperature
        const currentLocation = await getCurrentCoords();
        if (currentLocation) {
            currentWeather.value = await getSingleWeatherData(currentLocation);
        }
    });

    const handleForecast = async (newValue: number | null) => {
        // flush the forecast data if newValue is null
        if (newValue === null) {
            forecastData.value = null;
            return;
        }

        // fetch forecast data by city ID
        shouldGetForecast.value = newValue;
        const data = await getForecastData(newValue);
        forecastData.value = data;

        // clear shouldGetForecast state
        shouldGetForecast.value = null;
    };
</script>

<template>
    <div class="min-h-screen overflow-auto bg-cover dark:bg-neutral-900">
        <div class="w-4/6 h-screen mx-auto p-8">
            <div class="flex justify-between items-center">
                <div class="flex items-center gap-1">

                    <!-- using 3.svg since the app icon shown in table.png is not provided -->
                    <img
                        :src="`/icons/3.svg`"
                        :alt="'weather logo'"
                        class="w-10 mr-2"
                    />
                    <h1 class="text-xl font-semibold">Météo</h1>
                </div>

                <!-- display current location's temperature if currentWeather !== null -->
                <span class="flex items-center justify-end" v-if="currentWeather">
                    <UIcon name="i-heroicons-map-pin" class="w-6 h-6 mr-1" />
                    <p>{{ currentWeather }}</p>
                </span>
            </div>


            <div class="flex justify-between mt-16">
                <h1 class="text-4xl">Locations</h1>
                <UButton class="font-bold" @click="isModalOpen = true" color="black" variant="solid" label="+ Add Location"/>
            </div>

            <!-- main components and pass their required states -->
            <Table
                class="py-7"
                :locations="locations"
                :is-table-loading="isTableLoading"
                :is-sidebar-open="isSidebarOpen"
                :should-get-forecast="shouldGetForecast"
                @update:should-get-forecast="handleForecast"
                @update:is-sidebar-open="(newValue: boolean) => { isSidebarOpen=newValue }"
                @update:is-sidebar-loading="(newValue: boolean) => { isSidebarLoading=newValue }"
                @update:locations="(newLocations: WeatherObj[]) => { locations=newLocations }"
            />
            <Modal
                :is-modal-open="isModalOpen"
                :locations="locations"
                @update:is-modal-open="(newValue: boolean) => { isModalOpen=newValue }"
                @update:locations="(newLocations: WeatherObj[]) => { locations=newLocations }"
            />
            <Sidebar
                :is-sidebar-open="isSidebarOpen"
                :is-sidebar-loading="isSidebarLoading"
                :forecast-data="forecastData"
                @update:is-sidebar-open="(newValue: boolean) => { isSidebarOpen=newValue }"
                @update:is-sidebar-loading="(newValue: boolean) => { isSidebarLoading=newValue }"
                @update:forecast-data="handleForecast"
            />
            <UNotifications />
        </div>
    </div>

</template>
