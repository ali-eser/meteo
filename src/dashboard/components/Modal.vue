<script setup lang="ts">
    const { addLocation, searchLocation } = useWeatherApi();

    // useToast composable for adding notifications
    const toast = useToast();

    // store the modal input area value
    const modalValue = ref<string>("");

    // determine if the search box is loading
    const isLoading = ref<boolean>(false);

    // define props to be passed in
    const props = defineProps({
        // store locations fetched from the database
        locations: {
            type: Array,
            default: () => []
        },
        // determine if the add location modal is open or not
        isModalOpen: {
            type: Boolean,
            default: false
        }
    });

    // define emits to update external props
    const emit = defineEmits(["update:locations", "update:isModalOpen"]);

    // handle adding location
    const handleLocationAdd = async (city: string) => {
        try {
            // add location via POST /locations endpoint
            const response = await addLocation(city);

            // if response has a predefined error message, pop a notification and return
            if (Object.hasOwn(response, "error")){
                toast.add({
                    id: "error",
                    title: "Error",
                    description: response.error,
                    icon: "i-heroicons-x-circle"
                });
                return;
            }
            // create new locations state
            const newLocations = [...props.locations, response];

            // update the locations state with newLocations array, clear the input box, and close the modal
            emit("update:locations", newLocations);
            emit("update:isModalOpen", false);
            modalValue.value = '';

            // pop a success notification containing the name of the added location
            toast.add({
                id: "success",
                title: "Success",
                description: `${response.name} added successfully!`,
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
    }

    // handle searching for locations
    const search = async (city: string) => {
        // only query if the input box isn't empty
        if (city != "") {
            isLoading.value = true;
            // fetch matching location names via /locations/:city endpoint
            const capitals: string[] = await searchLocation(city);
            isLoading.value = false;
            return capitals;
        }
        // return an empty array if the input box is empty
        return [];
    }
</script>

<template>
    <div>
        <!-- only show modal if isModalOpen is true, and set isModalOpen to false upon closing. -->
        <!-- modal can also be closed by clicking anywhere else -->
        <UModal v-model="props.isModalOpen" @close="emit('update:isModalOpen', false)">
            <div class="flex justify-between mx-7 mt-7">
                <h1 class="text-3xl font-semibold">Add Location</h1>

                <!-- clear input value and close the modal when the close button is clicked -->
                <UButton
                    color="gray"
                    variant="solid"
                    icon="i-heroicons-x-mark-20-solid"
                    @click="() => {
                        emit('update:isModalOpen', false);
                        modalValue='';
                    }" />
            </div>
                <UInputMenu
                    icon="i-heroicons-magnifying-glass-20-solid"
                    :search="search"
                    :loading="isLoading"
                    class="mt-7 mx-7" color="gray" v-model="modalValue"
                    placeholder="Search for capital cities..."
                    size="xl"
                >

                    <!-- only show clear input button if a value from the dropdown is chosen -->
                    <template #trailing>
                        <UButton
                            v-show="modalValue !== ''"
                            color="gray"
                            variant="ghost"
                            icon="i-heroicons-x-mark-20-solid"
                            class="" @click="modalValue= ''" />
                    </template>

                    <!-- display a not found text if there are no matches -->
                    <template #option-empty="{ query }">
                        Capital city <q>{{ query }}</q> not found!
                    </template>
                </UInputMenu>

                <!-- only allow the user to add a location if they have chosen a city from the dropdown menu -->
                <UButton
                    v-bind:disabled="modalValue === ''"
                    class="mt-7 mb-7 mx-7 justify-center font-bold"
                    size="xl" color="black" variant="solid"
                    label="Add Location"
                    @click="handleLocationAdd(modalValue)"
                />
        </UModal>
    </div>
</template>
