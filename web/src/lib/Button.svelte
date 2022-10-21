<script>
  export let buttonText;
  export let buttonHandler;
  export let isDisabled = false;
</script>

<button
  class="p-4 rounded-md w-36 text-white text-center transition-all 
  {isDisabled ? 'bg-gray-600' : 'bg-blue-600 hover:bg-blue-500'}"
  on:click={buttonHandler()}
  disabled={isDisabled}
>
  {buttonText}
</button>
