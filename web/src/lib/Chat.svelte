<script>
  import Button from "./Button.svelte";
  import InputField from "./InputField.svelte";

  import { createEventDispatcher } from "svelte";
  import { validationMessages } from "../utils/constants";

  export let username;
  export let roomName;
  export let messages;
  export let isLoading;

  let chatRef;

  let message = "";

  let isFormValid = false;
  let validationErrors = {
    message: "",
  };

  let dirtyFields = {
    message: false,
  };

  $: {
    if (message === "" && dirtyFields.message) {
      validationErrors.message = validationMessages.required;
    } else {
      validationErrors.message = "";
    }

    isFormValid = Object.values(validationErrors).every(
      (value) => value === ""
    );
  }

  $: fieldsUntouched = Object.values(dirtyFields).some(
    (value) => value === false
  );

  $: if (messages && chatRef) {
    const chatElementSize = 56
    // Add a timeout to allow the DOM to update
    setTimeout(() => {
        const isAtBottom = chatRef.scrollTop === (chatRef.scrollHeight - chatRef.offsetHeight - chatElementSize);

        // If the user is at the bottom of the chat, scroll to the bottom
        if (isAtBottom) {
          scrollToBottom()
        }
    }, 1)
  }

  function scrollToBottom() {
    chatRef.scroll({ top: chatRef.scrollHeight, behavior: "smooth" });
  }

  const dispatch = createEventDispatcher();

  function handleSendMessage() {
    if (fieldsUntouched && !message) {
      Object.keys(dirtyFields).forEach((key) => {
        dirtyFields[key] = true;
      });
      return;
    }

    if (!isFormValid) {
      return;
    }

    const messagePayload = {
      username,
      roomName,
      message,
    };

    dispatch("sendChatMessage", messagePayload);

    message = "";
    dirtyFields.message = false;
  }
</script>

<div class="flex-1 flex-grow flex flex-col h-full">
  <h4
    class="font-extrabold text-4xl text-transparent bg-clip-text bg-gradient-to-r from-blue-300 to-blue-600"
  >
    Room: {roomName}
  </h4>
  <div bind:this={chatRef} class="flex-grow overflow-y-auto">
    <div class="max-h-64">
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
  </div>

  <div class="flex flex-col gap-4 mb-6 flex-0">
    <InputField
      bind:value={message}
      placeholder="Say something interesting"
      error={validationErrors.message}
      on:becomeDirty={() => (dirtyFields.message = true)}
      id={"message_input"}
      on:keypress={(e) => {
        const key = e.detail;

        if (key === "Enter") {
          handleSendMessage();
        }
      }}
    />

    <Button
      isDisabled={isLoading}
      buttonText={(isLoading && "Loading...") || "Send"}
      buttonHandler={handleSendMessage}
    />
  </div>
</div>
