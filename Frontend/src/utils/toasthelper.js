import { toasts } from "svelte-toasts";

export function showToast(title, body, theme) {
  toasts.add({
    title,
    description: body,
    duration: 3000,
    type: theme,
    placement: "bottom-right",
    showProgress: true,
    onClick: () => {},
    onRemove: () => {},
  });
}