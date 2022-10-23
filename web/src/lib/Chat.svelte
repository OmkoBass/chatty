<script>
  import Button from "./Button.svelte";
  import InputField from "./InputField.svelte";

  import { createEventDispatcher } from "svelte";

  export let username;
  export let roomName;
  export let messages;
  export let isLoading;

  let message = "";

  const dispatch = createEventDispatcher();

  function handleSendMessage() {
    dispatch("sendChatMessage", {
      username,
      roomName,
      message,
    });
    message = "";
  }
</script>

<div class="flex flex-col justify-between">
  <h4
    class="font-extrabold text-4xl text-transparent bg-clip-text bg-gradient-to-r from-blue-300 to-blue-600"
  >
    Room: {roomName}
  </h4>

  <div class="flex-grow">
    {#each messages as message}
      <section class="mb-2">
        <h4
          class="{message.username === username
            ? 'text-transparent bg-clip-text bg-gradient-to-r from-pink-500 to-orange-500'
            : 'text-gray-300'} font-extrabold"
        >
          {message.username}
        </h4>
        <p class="text-gray-300">{message.message}</p>
      </section>
    {/each}
  </div>

  <div class="grid gap-6 mb-6">
    <InputField
      bind:value={message}
      placeholder="Say something interesting"
      id={"message_input"}
    />

    <Button
      isDisabled={isLoading}
      buttonText={(isLoading && "Loading...") || "Send"}
      buttonHandler={handleSendMessage}
    />
  </div>
</div>
