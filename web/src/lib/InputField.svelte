<script>
  export let id;
  export let label = "";
  export let value;
  export let placeholder;
  export let disabled = false;
</script>

<div>
  <label for={id} class="block mb-2 text-sm font-medium text-gray-300"
    >{label}</label
  >
  <input
    autocomplete="off"
    type="text"
    {id}
    class="border text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 bg-gray-700 border-gray-600 placeholder-gray-400 text-white"
    {placeholder}
    {disabled}
    bind:value
  />
</div>
