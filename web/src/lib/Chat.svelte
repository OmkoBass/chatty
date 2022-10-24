<script>
  import Button from "./Button.svelte";
  import InputField from "./InputField.svelte";

  import { createEventDispatcher } from "svelte";
  import { validationMessages } from "../utils/constants";

  export let username;
  export let roomName;
  export let messages;
  export let isLoading;

  let message = "";

  let isFormValid = false;
  let validationErrors = {
    message: '',
  }

  let dirtyFields = {
    message: false
  }

  $: {
    if(message === '' && dirtyFields.message) {
      validationErrors.message = validationMessages.required;
    } else {
      validationErrors.message = '';
    }

    isFormValid = Object.values(validationErrors).every((value) => value === '');
  }

  $: fieldsUntouched = Object.values(dirtyFields).some((value) => value === false);

  const dispatch = createEventDispatcher();

  function handleSendMessage() {
    if(fieldsUntouched) {
      Object.keys(dirtyFields).forEach((key) => {
        dirtyFields[key] = true;
      });
      return
    }

    if (!isFormValid) {
      return
    }

    const messagePayload = {
      username,
      roomName,
      message
    }

    dispatch("sendChatMessage", messagePayload);

    message = "";
    dirtyFields.message = false;
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
      error="{validationErrors.message}"
      on:becomeDirty={() => dirtyFields.message = true}
      id={"message_input"}
    />

    <Button
      isDisabled={isLoading}
      buttonText={(isLoading && "Loading...") || "Send"}
      buttonHandler={handleSendMessage}
    />
  </div>
</div>
