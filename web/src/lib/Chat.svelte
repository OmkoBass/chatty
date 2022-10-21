<script>
  import Button from "./Button.svelte";

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
      room: roomName,
      message,
    });
    message = "";
  }
</script>

<div class="flex flex-col justify-center w-full">
  <h4 class="text-center my-4 font-bold">You are {username}</h4>
  <h4 class="text-center font-bold">Room: {roomName}</h4>

  {#each messages as message}
    <h4 class="my-2">
      <span class="font-bold">{message.username}:</span>{message.message}
    </h4>
  {/each}

  <div>
    <input
      class="my-4"
      type="text w-full"
      placeholder="I never lose"
      bind:value={message}
    />
  </div>

  <Button
    isDisabled={isLoading}
    buttonText={(isLoading && "Loading...") || "Send"}
    buttonHandler={handleSendMessage}
  />
</div>
