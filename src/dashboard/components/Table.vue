<script setup lang="ts">
    import type { WeatherObj } from '~/types';
    import type { PropType } from 'vue';

    // import useWeatherApi composable
    const { deleteLocation } = useWeatherApi();

    // useToast composable for adding notifications
    const toast = useToast();

    // determine if the location removal confirmation modal is opened or not
    const isConfirmationOpen = ref<boolean>(false);

    // store the ID of the location to remove
    const locationToRemove = ref<number | null>(null);

    // determine if the page is initially loaded for the first time
    const isInitialLoad = ref<boolean>(true);

    // define props to be passed in
    const props = defineProps({
        // determine if table is fetching data
        isTableLoading: {
            type: Boolean,
            default: false
        },
        // store locations fetched from the database
        locations: {
            type: Array as PropType<WeatherObj[]>,
            default: () => []
        },
        // determine if the sidebar is open or not
        isSidebarOpen: {
            type: Boolean,
            default: false
        },
        // determine if the sidebar is loading data
        isSidebarLoading: {
            type: Boolean,
            default: false
        },
        // determine if the app should fetch forecast data or no
        shouldGetForecast: {
            type: [Number, null] as PropType<number | null>,
            default: null
        }
    });
    // define emits to update values of isSidebarOpen, shouldGetForecast, and locations states
    const emit = defineEmits(["update:isSidebarOpen", "update:isSidebarLoading", "update:shouldGetForecast", "update:locations"])

    // define table columns
    const columns = [
        { key: "name", label: "Location" },
        { key: "temperature", label: "Temperature" },
        { key: "rain", label: "Rainfall" },
        // actions column for location removal button
        { key: "actions", label: "" }
    ];

    // set default page number to 1
    const page = ref<number>(1);

    // show maximum of 10 locations per page by slicing the locations array
    const maxPerPage = 10;
    const rows = computed(() => {
        return props.locations.slice((page.value - 1) * maxPerPage, (page.value) * maxPerPage);
    });

    // automatically change pages on location addition and removal by tracking locations count
    watch(() => props.locations, (newValue, oldValue) => {
        // if page loaded and locations set for the first time, show the first page
        if (isInitialLoad.value) {
            page.value = 1;
            isInitialLoad.value = false;
            return;
        }

        // if a location is added, go to the last page where the new location will be
        if (newValue.length > oldValue.length) {
            page.value = Math.ceil(newValue.length / maxPerPage);
        }
        // if a location is removed check whether or not the page count has decreased
        else if (newValue.length < oldValue.length) {
            const maxPage = Math.ceil(newValue.length / maxPerPage);

            // if so, go to the previous page
            if (page.value > maxPage) {
                page.value = maxPage;
            }
        }
    });

    // when a row is clicked on, open the sidebar and update shouldGetForecast state with corresponding ID
    const select = async (row: WeatherObj) => {
        emit("update:isSidebarOpen", true);
        emit("update:isSidebarLoading", true);
        emit("update:shouldGetForecast", row.id);
    };

    // when a remove button is clicked, update locationToRemove state with corresponding ID
    // and open the removal confirmation modal
    const openRemoveConfirmation = (id: number) => {
        locationToRemove.value = id;
        isConfirmationOpen.value = true;
    };

    // handle the removal of a location
    const handleLocationRemoval = async () => {
        if (locationToRemove.value === null) return;
        try {
            // define new locations array without the removed location
            const newLocations = props.locations.filter(l => l.id !== locationToRemove.value);

            // remove location from the database via DELETE /locations/:location_id endpoint
            const response = await deleteLocation(locationToRemove.value);

            // if the response has a predefined error message, pop a notification and return
            if (Object.hasOwn(response, "error")) {
                toast.add({
                    id: "error",
                    title: "Error",
                    description: response.error,
                    icon: "i-heroicons-x-circle"
                });
                return;
            }
            // update the locations state with the newly created locations array
            emit("update:locations", newLocations);

            // close the confirmation modal and clear the locationToRemove state
            isConfirmationOpen.value = false;
            locationToRemove.value = null;

            // pop a success notification containing the name of the removed location
            toast.add({
                id: "success",
                title: "Success",
                description: response.message,
                icon: "i-heroicons-check-badge"
            });
        // catch any non predefined error messages and pop a notification containing the error
        } catch (error) {
            toast.add({
                id: "error",
                title: "Error",
                description: `An unexpected error: ${error} occured.`,
                icon: "i-heroicons-x-circle"
            });
        }
    };
</script>

<template>
    <div class="flex-col justify-between">
        <div class="rounded overflow-hidden">
            <!-- define table and its empty and loading states -->
            <UTable
                :empty-state="{
                    icon: 'i-heroicons-circle-stack-20-solid',
                    label: 'No locations found. Press the \'+ Add Location\' button to add one.' 
                }"
                :loading="props.isTableLoading"
                :loading-state="{
                    icon: 'i-heroicons-arrow-path-20-solid',
                    label: 'Fetching locations...' 
                }"
                :columns="columns"
                @select="select"
                :rows="rows"
            >
                <template #name-data="{ row }">
                    <div class="flex items-center gap-3 w-24">

                        <!-- show a weather icon corresponding to the mapped weather code -->
                        <img
                            :src="`/icons/${row.weather_code}.svg`"
                            :alt="`weather icon ${row.weather_code}`"
                            class="w-8 h-8"
                        />

                        <!-- make location name bolder -->
                        <span class="font-semibold">{{ row.name }}</span>
                    </div>
                </template>

                <!-- show a remove button with a trash icon aligned to right -->
                <template #actions-data="{ row }">
                    <div class="flex justify-end">
                        <UButton
                            color="gray"
                            variant="ghost"
                            icon="i-heroicons-trash"
                            size="sm"
                            @click.stop="openRemoveConfirmation(row.id)"
                            aria-label="Delete"
                        />
                    </div>
                </template>
            </UTable>
        </div>

        <!-- set pagination according to the defined max item per page count -->
        <!-- and only show pagination if there are at least a couple of pages -->
        <div v-if="props.locations.length > 10" class="flex justify-end px-3 py-3.5">
            <UPagination v-model="page" :page-count="maxPerPage" :total="props.locations.length" />
        </div>

        <!-- confirmation modal shown when the remove button is clicked -->
        <UModal v-model="isConfirmationOpen">
            <div class="px-16 py-7 font-semibold">
                <h3 class="text-2xl text-center">Are you sure you want to remove?</h3>
                <div class="flex justify-around mt-7">

                    <!-- clicking remove removes the location, clicking cancel closes the modal and clears locationToRemove state -->
                    <UButton class="w-36 justify-center" label="Remove" @click="handleLocationRemoval"/>
                    <UButton class="w-36 justify-center" label="Cancel"
                            @click="() => {
                                isConfirmationOpen=false;
                                locationToRemove=null;
                            }"/>
                </div>
            </div>
        </UModal>
    </div>
</template>
