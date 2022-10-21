import type { Message } from "../../types";
import { socketActions } from "../../enums/index";

export function sendMessage(socket, message: Message) {
  socket.emit(socketActions.sendMessage, message);
}
