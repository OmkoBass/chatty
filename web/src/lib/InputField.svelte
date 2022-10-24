<script>
  import { createEventDispatcher } from "svelte";

  export let id;
  export let label = "";
  export let value;
  export let placeholder;
  export let disabled = false;
  export let error = "";

  let isDirty = false

  $: hasError = error !== "";

  const dispatch = createEventDispatcher()

  function handleBecomeDirty() {
    if (isDirty) {
      return
    }

    isDirty = true
    dispatch('becomeDirty', {
      isDirty
    })
  }
</script>

<div>
  <label for={id} class="block mb-2 text-sm font-medium text-gray-300"
    >{label}</label
  >
  <input
    autocomplete="off"
    type="text"
    {id}
    class="{hasError && 'focus:border-red-500 border-red-500'} border text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 bg-gray-700 border-gray-600 placeholder-gray-400 text-white"
    {placeholder}
    {disabled}
    bind:value
    on:input={handleBecomeDirty}
  />
  <p class="text-red-500">{error}</p>
</div>
