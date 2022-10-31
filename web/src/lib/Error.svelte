<script>
    export let errorMessage
    export let isVisible
</script>

{#if isVisible}
    <pre class="text-red-500">{JSON.stringify(
        errorMessage,
        null,
        4
    )}</pre>
{/if}
