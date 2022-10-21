import { ChatAction } from "../../types";
import { socketActions } from "../../enums/index";

export function joinRoom(socket, chatAction: ChatAction) {
  socket.emit(socketActions.joinRoom, chatAction);
}
